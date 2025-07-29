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
from mortgagemodeler import Loan

loan = Loan.from_fixed(principal=400000, rate=0.065, term_years=30)
loan.plot_amortization()
```

## CLI Usage

Run amortization simulations via CLI:

```bash
mortgagemodeler simulate --principal 400000 --rate 6.5 --term 30
```

Use `--help` to see all available options.

## Features

- Fixed-rate, ARM, FHA, and HELOC support
- Recast and refinance simulation logic
- Cost comparison based on exit year or refinance timing
- Monthly and annual amortization tables with CSV export
- Matplotlib-based amortization plots
- Python API and CLI tool (`mortgagemodeler`)
- Easily extendable for other loan types and policies

## Example Notebooks

This repo includes ready-to-run Jupyter examples in the `notebooks/` folder:

- **Fixed_vs_ARM.ipynb**: Compare fixed vs adjustable-rate loan paths
- **FHA_vs_Conventional.ipynb**: Analyze MIP vs PMI cost impact
- **Refinance_Breakeven.ipynb**: Estimate the optimal time to refinance

Launch directly in Binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/arunkpe/mortgagemodeler/HEAD?labpath=notebooks%2FFixed_vs_ARM.ipynb)

## License

MIT License © 2025 Arun Kumar