# ARES 3.0.5

To develop ARES, the Agency collected data from annual financial statements as part of requests to 16 second-tier banks. The data received included information on the financial indicators of legal entity borrowers whose debt exceeded 100 million tenge. At the same time, the request consisted of two groups: borrowers that defaulted in the period from 01.10.2014 to 01.01.2020 (default) and borrowers who did not default as of 01.01.2021 (standard).

## ARES: Advanced Toolkit for Financial and Non-financial Data Assessment

This release is an updated and restructured version of our previously published ML test model. It reflects continued development efforts aimed at enhancing the model’s applicability in real-world credit risk assessment tasks. The core structure remains based on the integration of both quantitative financial indicators and qualitative borrower attributes, such as audit status, legal proceedings, and external ratings. This hybrid approach ensures a more comprehensive and accurate evaluation of default risk. The current release includes improvements in dataset consistency, additional control procedures, refined model functions, and updated documentation. These enhancements are part of a broader effort to transition from a prototype to a fully functional statistical tool designed for use by risk analysts, banking professionals, and researchers.

ARES is a comprehensive analytical toolkit designed to support statisticians, financial analysts, data scientists, and banking professionals in the processing and interpretation of structured financial and macroeconomic datasets. Developed by the Agency of the Republic of Kazakhstan for Regulation and Development of the Financial Market (ARDFM), ARES facilitates a data-driven approach to credit risk evaluation.

## Key capabilities of ARES include:

- Structured loading and automated validation of financial datasets  
- Computation and analysis of core financial ratios  
- Development and performance assessment of regression models  
- Implementation of statistical diagnostics and hypothesis testing  
- Estimation of default probabilities based on empirical data  

## Authors

**Aryslan Iskakov** – Maintainer, Team Lead of Financial Market Cyber Resilience Department, ARDFM  
Contact: iskakov.aryslan@gmail.com

## Built-in Datasets

**factorsKZ**  
Financial and non-financial ratios of corporate borrowers classified as default or standard (IFRS stage 1), collected during the Asset Quality Review (AQR) procedure in Kazakhstan.

### Variables include:
- Default: `0 = standard`, `1 = default`
- Growth: `Rev_gr`, `EBITDA_gr`, `Cap_gr`
- Liquidity: `CR`, `QR`, `Cash_ratio`
- Leverage: `DTA`, `DTE`, `LR`, `EBITDA_debt`, `IC`, etc.
- Profitability: `ROA`, `ROE`, `NPM`, `GPM`, `OPM`
- Turnovers: `RecT`, `InvT`, `PayT`, `TA`, `FA`, `WC`
- Non-financial data: `LI`, `AuditSt`, `ExtRtg`

### Usage:
```python
import pandas as pd
from ares_afr import load_factors
df = load_factors()
```

### Reference:
Agency of the Republic of Kazakhstan for Regulation and Development of Financial Market

## Installation

```bash
pip install ares_afr
```

## License

This project is licensed under the BSD 3-Clause License. See the LICENSE file for more information.  
Copyright: The Agency of the Republic of Kazakhstan for Regulation and Development of Financial Market