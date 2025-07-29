from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd

from mortgagemodeler.utils.interest import calculate_interest
from mortgagemodeler.utils.rates import RateReader


class LoanAmortizer:
    """
    LoanAmortizer builds an amortization schedule for various loan types including:
    - Fixed Rate Loans
    - Adjustable Rate Mortgages (ARMs)
    - FHA Loans with MIP
    - VA and USDA Loans with Guarantee Fees
    - HELOCs with draw and repayment phases

    It supports:
    - Custom forward rate schedules
    - Insurance premiums (PMI, MIP, USDA annual fee)
    - Extra principal payments
    - Balloon payments
    - Monthly or biweekly payment frequencies
    - Mid-life loan entry (starting at a custom month and balance)
    - Decimal-based precision for all financial calculations

    Parameters
    ----------
    loan : Loan
        An instance of the Loan class with fully defined parameters.
    custom_rate_schedule : dict, optional
        A dictionary mapping date strings ("YYYY-MM-DD") to interest rate overrides.
    start_month : int, optional
        The month index to begin amortizing from (defaults to 1).
    starting_balance : Decimal, optional
        The loan balance to begin amortizing from (defaults to loan.principal).
    starting_date : datetime.date, optional
        The calendar date to begin amortizing from (defaults to loan.origination_date).
    """
    def __init__(self, loan, custom_rate_schedule=None, start_month=1, starting_balance=None, starting_date=None):
        self.loan = loan
        self.schedule = []
        self.initial_rate = loan.rate
        self.last_rate = loan.rate
        self.custom_rate_schedule = custom_rate_schedule or {}
        self.rates = RateReader() if loan.loan_type in ['arm', 'heloc'] else None

        self.start_month = start_month
        self.starting_balance = Decimal(starting_balance) if starting_balance else loan.principal
        self.starting_date = starting_date or loan.origination_date

        self._build_amortization()

    def _get_effective_rate(self, date_str: str, month: int) -> Decimal:
        """
        Returns the effective interest rate for a given date.
        - Applies user-defined rate override if available
        - Applies forward curve rate if defined
        - Falls back to fixed rate or ARM index + margin logic
        - Enforces ARM caps and floors on reset months

        Parameters
        ----------
        date_str : str
            Date in YYYY-MM-DD format.
        month : int
            Month index in loan lifecycle (1-indexed)

        Returns
        -------
        Decimal
            Effective annual interest rate for that period.
        """
        if date_str in self.custom_rate_schedule:
            return Decimal(str(self.custom_rate_schedule[date_str]))

        if self.loan.forward_curve and date_str in self.loan.forward_curve:
            return Decimal(str(self.loan.forward_curve[date_str]))

        if self.loan.loan_type == 'fixed':
            return self.loan.rate

        if self.loan.loan_type in ['arm', 'heloc'] and self.loan.index and self.rates:
            try:
                base_rate = Decimal(str(self.rates.get_rate(self.loan.index, date_str)))
            except Exception:
                base_rate = self.last_rate - self.loan.margin

            proposed = (base_rate + self.loan.margin).quantize(Decimal("0.0001"))

            fixed_months = self.loan.arm_structure[0] * 12
            reset_freq = self.loan.arm_structure[1]

            is_reset_month = (
                month > fixed_months and
                (month - fixed_months) % reset_freq == 0
            )

            if is_reset_month:
                cap = Decimal(self.loan.caps['periodic'])
                floor = Decimal(self.loan.rate_bounds.get('periodic_floor', 0))
                upper = self.last_rate + cap
                lower = self.last_rate - cap
                capped = min(max(proposed, lower), upper)

                max_life = Decimal(self.loan.caps['lifetime'])
                min_life = Decimal(self.loan.rate_bounds.get('lifetime_floor', 0))
                life_upper = self.initial_rate + max_life
                life_lower = self.initial_rate - min_life
                capped = min(max(capped, life_lower), life_upper)

                self.last_rate = capped
                return capped

            return self.last_rate

        return self.loan.rate

    def _calculate_insurance(self, balance: Decimal, month: int) -> Decimal:
        """
        Calculate monthly insurance (MIP, PMI, or USDA annual fee) based on loan type.

        Parameters
        ----------
        balance : Decimal
            Current outstanding balance.
        month : int
            Current month number in the loan term.

        Returns
        -------
        Decimal
            Monthly insurance premium amount.
        """
        if self.loan.is_fha:
            return (balance * self.loan.fha_monthly).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        elif self.loan.is_usda:
            return (balance * self.loan.usda_annual_fee / Decimal("12")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        elif self.loan.is_pmi:
            ltv = balance / self.loan.original_balance
            if ltv <= Decimal("0.78") or month > 132:
                return Decimal("0.00")
            return (balance * self.loan.pmi_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Decimal("0.00")

    def _build_amortization(self):
        """
        Constructs the full amortization schedule from start date through maturity.

        Handles:
        - Draw period and interest-only payments (HELOC)
        - Full amortization including principal + interest
        - Monthly insurance additions
        - Extra payments and biweekly payment approximation
        - Accurate payment calculations using present value formula
        """
        balance = self.starting_balance
        current_date = self.starting_date
        total_term = self.loan.term
        draw_period = self.loan.draw_period_months
        repay_term = self.loan.repayment_term_months or (total_term - draw_period)
        extra_amt = self.loan.extra_payment_amount
        frequency = self.loan.extra_payment_frequency or 'monthly'

        for month in range(self.start_month, total_term + 1):
            current_date += timedelta(days=30)
            date_str = current_date.strftime('%Y-%m-%d')

            rate = self._get_effective_rate(date_str, month)
            interest = Decimal(calculate_interest(balance, rate, 30, self.loan.compounding)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            if self.loan.is_heloc and month <= draw_period:
                payment = interest
                principal = Decimal("0.00")
            else:
                monthly_rate = rate / Decimal("12") / Decimal("100")
                if self.loan.is_heloc:
                    remaining_term = repay_term - (month - draw_period - 1)
                else:
                    remaining_term = total_term - month + 1
                payment = (balance * monthly_rate / (1 - (1 + monthly_rate) ** -remaining_term)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                principal = (payment - interest).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            if frequency == 'biweekly':
                extra = (extra_amt * Decimal("26") / Decimal("12")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            else:
                extra = extra_amt

            insurance = self._calculate_insurance(balance, month)
            total_payment = (payment + insurance + extra).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_principal = principal + extra
            ending_balance = max((balance - total_principal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), Decimal("0.00"))

            self.schedule.append({
                "Month": month,
                "Date": date_str,
                "Beginning Balance": float(balance),
                "Payment": float(payment),
                "Principal": float(principal),
                "Interest": float(interest),
                "PMI/MIP": float(insurance),
                "Extra Payment": float(extra),
                "Total Payment": float(total_payment),
                "Ending Balance": float(ending_balance)
            })

            balance = ending_balance

            if balance <= Decimal("0.00"):
                break

    def to_dataframe(self):
        """
        Returns the amortization schedule as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            Tabular amortization schedule.
        """
        return pd.DataFrame(self.schedule)

    def to_csv(self, filepath):
        """
        Writes the amortization schedule to a CSV file.

        Parameters
        ----------
        filepath : str
            Destination file path.
        """
        self.to_dataframe().to_csv(filepath, index=False)
