# Logi-Health Dashboard
_Open-source Streamlit app that turns raw trucking KPIs into actionable fleet insights_

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b)

## What is this?
Logi-Health Dashboard ingests a monthly driver dataset (4,814 rows × 17 columns in the demo)  
and delivers an interactive web app + slide-ready PDF that answer:

* **Where are our riskiest depots?** (Safety Score)
* **Which sites are over- or under-staffed?** (Workload Score)
* **Which locations will likely deteriorate next quarter?** (Time-series trend detection)

All logic is packaged in reusable Python classes—**`SafetyScoreCalculator`** and **`WorkloadScoreCalculator`**—so you can plug in any similar fleet dataset.


## Features
| Module | What it does |
|--------|--------------|
| **SafetyScoreCalculator** | `1 – [(Preventable + Duty + Training) / Driver Ct]` — highlights rule-breaking hotspots |
| **WorkloadScoreCalculator** | `1 – |Avg Weekly Hours – Target| / Target` (default Target = 50 hrs) |
| **Trend Detector** | Rolling OLS + SciPy trend test → flags KPIs on a worsening trajectory |
| **Streamlit UI** | Top / Bottom-10 bar charts, distribution plots, location drill-down |
| **PDF exporter** | One-click WeasyPrint → share with execs without sending a link |

## Tech stack
* **Python 3.10+**
* `streamlit 1.35`
* `pandas`, `numpy`
* `plotly`, `seaborn`
* `scipy`, `statsmodels`
* `weasyprint 59` (+ `pydyf`)
* `openpyxl` (Excel ingest)

## Quick start
```bash
# 1. Clone repo & create virtual env
git clone https://github.com/<your-user>/logi-health-dashboard.git
cd logi-health-dashboard
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place your monthly KPI file(s) in ./data/
#    Expected columns include:
#    LocationID, YEAR_MONTH, Driver Ct, Duty Violation Ct, Preventable incident Ct,
#    Past due training Ct, Avg Weekly Hours, …
#    (see docs/column_definitions.md for full spec)

# 4. Launch Streamlit app
streamlit run app.py
