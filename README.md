# EconoCausal: Dynamic Pricing via Double Machine Learning

## Project Overview

EconoCausal investigates how experimental electricity price signals may affect household electricity consumption. The project uses electricity-pricing experiment data to explore consumption patterns and, where the experiment design and data support it, estimate causal effects using **Double Machine Learning (DoubleML)**.

The aim is to go beyond predicting consumption and investigate whether changes in price signals are associated with changes in hourly household electricity demand.

> **Project status:** In progress. Findings and causal estimates will be added after data validation and analysis. No results are claimed in this README.

## Research Question

**How do experimental electricity price signals affect hourly household electricity consumption?**

## Objectives

- Understand the electricity-pricing experiment and its datasets.
- Inspect, clean, and prepare data for analysis.
- Explore hourly electricity consumption, price signals, and temperature patterns.
- Define the treatment, outcome, and appropriate control variables.
- Assess whether the experiment design supports a credible causal analysis.
- Apply Double Machine Learning if its assumptions and the available data support the approach.
- Build an interactive dashboard after the mid-review.
- Communicate the findings through a report, presentation, and project demonstration.

## Dataset

This project uses the **iFlex dynamic electricity pricing experiment dataset**.

- **Source:** [iFlex dataset on Zenodo](https://zenodo.org/records/8248802)
- **DOI:** [10.5281/zenodo.8248802](https://doi.org/10.5281/zenodo.8248802)
- **Context:** Household smart-meter electricity consumption and experimental price signals, with related time and temperature information.

### Files currently selected

| File | Purpose |
|---|---|
| `experiment_days.csv` | Experiment dates, participation phases, price signals, and groups |
| `price_signals.csv` | Price profiles, price levels, hours, and experimental prices |

The larger hourly consumption file, `data_hourly.csv`, is intended for the main analysis. It contains fields such as household ID, date/time, electricity demand, price signal, experimental price, and temperature measures.

**Data access note:** The hourly dataset is large. Download it from the official source as needed; avoid committing large raw data files to GitHub. Keep local data files out of version control unless there is a clear reason and the repository can support them.

## Planned Methodology

1. **Dataset inspection** — inspect the structure, data types, date coverage, missing values, and duplicates.
2. **Preprocessing** — validate timestamps and variables, address data-quality issues, and prepare analysis-ready data.
3. **Exploratory Data Analysis (EDA)** — examine consumption by hour and date, price patterns, temperature, and experimental groups.
4. **Causal design** — identify the treatment, outcome, and relevant covariates, and verify how price signals were assigned.
5. **Causal estimation** — use DoubleML and suitable machine-learning nuisance models only if the data and identification assumptions justify it.
6. **Validation and interpretation** — assess uncertainty, robustness, and limitations; avoid interpreting association as causation without adequate support.
7. **Dashboard and communication** — develop a Streamlit dashboard with Plotly visualizations, then prepare the report, presentation, and demo.

## Planned Technology Stack

- **Language:** Python
- **Data processing:** Pandas, NumPy
- **Analysis and machine learning:** scikit-learn, DoubleML (subject to suitability checks)
- **Visualization:** Plotly, Matplotlib
- **Interactive dashboard:** Streamlit
- **Development environment:** Jupyter Notebook / VS Code
- **Version control:** Git and GitHub

## Repository Structure

The repository structure will grow as the project progresses. A planned layout is:

```text
EconoCausal/
├── README.md
├── data/
│   └── README.md              # Data download and access instructions
├── notebooks/
│   ├── 01_dataset_inspection.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_causal_analysis.ipynb
├── src/                       # Reusable analysis code
├── dashboard/                 # Streamlit dashboard (after mid-review)
├── reports/                   # Report, figures, and presentation materials
└── requirements.txt            # Project dependencies
```

This is a planned structure; folders and files will be added as they are created.

## Expected Deliverables

- Reproducible data inspection and preprocessing code
- Exploratory analysis and visualizations
- A documented causal analysis plan and validated estimates, if supported by the data
- Interactive Streamlit dashboard
- Final project report and presentation
- Demonstration of the completed project

## Current Progress

- [x] Selected the iFlex electricity-pricing experiment dataset.
- [x] Downloaded `experiment_days.csv` and `price_signals.csv`.
- [ ] Document the project objectives and repository setup.
- [ ] Inspect the selected CSV files.
- [ ] Load and prepare the hourly consumption data.
- [ ] Complete EDA and document observations.
- [ ] Validate the causal design and estimate effects if appropriate.
- [ ] Build the dashboard after the mid-review.
- [ ] Complete the report, presentation, and demo.

## Important Note

The causal conclusions of this project depend on the experiment design, treatment assignment, data quality, and statistical assumptions. The analysis will document these checks and limitations before presenting any causal claims.

## Acknowledgment

The project uses the iFlex dataset made available through Zenodo. Please refer to the [official dataset record](https://zenodo.org/records/8248802) for the dataset description, citation, and usage information.
