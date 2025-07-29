# MortgageModeler

**MortgageModeler** is a modular Python toolkit for modeling mortgage amortization, refinancing, FHA loans, and HELOCs — complete with CLI support and plotting.

[![PyPI](https://img.shields.io/pypi/v/mortgagemodeler)](https://pypi.org/project/mortgagemodeler/)
[![GitHub](https://img.shields.io/badge/github-arunkpe/mortgagemodeler-blue)](https://github.com/arunkpe/mortgagemodeler)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/arunkpe/mortgagemodeler/HEAD?labpath=notebooks%2FFixed_vs_ARM.ipynb)

**MortgageModeler** lets you simulate mortgage payments over time, compare fixed vs ARM loans, evaluate refinance and recast scenarios, and export visualizations or CSVs — all from Python or the command line.

## Installation

Install from PyPI:

```bash
pip install mortgagemodeler
```

## Quickstart

Using the Python API:

```python
from mortgagemodeler import Loan, LoanAmortizer

loan = Loan(principal=400000, rate=0.0625, term_months=360, origination_date="2023-01-01")
amortizer = LoanAmortizer(loan)
amortizer.plot()
```

## CLI Usage

Run amortization calculations and models via CLI:

```bash
mortgagemodeler amortize --balance 400000 --rate 6.25 --term 360 --type arm \
  --index SOFR --margin 2.75 --arm-structure 5 6 --caps 2 1 5 --floors 0 0 0 \
  --start-date 2023-01-01 --extra-payment 100 --show-apr --plot

mortgagemodeler amortize --help
```

Use `--help` to see all available options.

## Features

- Fixed-rate, ARM, FHA, and HELOC support
- Recast and refinance simulation logic
- Cost comparison based on exit year or refinance timing
- Compare APRs including discount points and fees
- Monthly and annual amortization tables with CSV export
- CSV export, JSON output, and matplotlib visualizations
- Matplotlib-based amortization plots
- Python API and CLI tool for scripting and terminal workflows (`mortgagemodeler`)
- Easily extendable for other loan types and policies


## Example Notebooks

Check github repowhich  includes ready-to-run Jupyter examples in the `examples/` folder:

- **Fixed_vs_ARM.ipynb**: Compare fixed vs adjustable-rate loan paths
- **FHA_vs_Conventional.ipynb**: Analyze MIP vs PMI cost impact
- **Refinance_Breakeven.ipynb**: Estimate the optimal time to refinance

Launch directly in Binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/arunkpe/mortgagemodeler/HEAD?labpath=notebooks%2FFixed_vs_ARM.ipynb)

## License

MIT License © 2025 Arun Kumar