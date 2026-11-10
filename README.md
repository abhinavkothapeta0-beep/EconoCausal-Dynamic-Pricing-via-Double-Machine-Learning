# EconoCausal: Dynamic Pricing via Double Machine Learning

## Project Overview

EconoCausal investigates how experimental electricity price signals may affect household electricity consumption. The project uses electricity-pricing experiment data to explore consumption patterns and, where the experiment design and data support it, estimate causal effects using **Double Machine Learning (DoubleML)**.

The aim is to go beyond predicting consumption and investigate whether changes in price signals are associated with changes in hourly household electricity demand.

**Project Status:** In progress. Findings and causal estimates will be added after data validation and analysis. No results are claimed in this README.

## Research Question

**How do experimental electricity price signals affect hourly household electricity consumption?**

## Objectives

- Understand the electricity-pricing experiment and its datasets.
- Inspect, clean, and prepare data for analysis.
- Explore hourly electricity consumption, price signals, and temperature patterns.
- Define the treatment, outcome, and appropriate control variables.
- Assess whether the experiment design supports a credible causal analysis.
- Apply Double Machine Learning if its assumptions and available data support the approach.
- Build an interactive dashboard after the mid-review.
- Communicate findings through a report, presentation, and project demonstration.

## Dataset

This project uses the **iFlex dynamic electricity pricing experiment dataset**.

- **Source:** [iFlex Dataset on Zenodo](https://zenodo.org/records/8248802)
- **DOI:** [10.5281/zenodo.8248802](https://doi.org/10.5281/zenodo.8248802)
- **Context:** Household smart-meter electricity consumption and experimental price signals, with related time and temperature information.

### Files Currently Selected

| File | Purpose |
|---|---|
| `experiment_days.csv` | Experiment dates, participation phases, price signals, and groups |
| `price_signals.csv` | Price profiles, price levels, hours, and experimental prices |

The larger hourly consumption file, `data_hourly.csv`, is intended for the main analysis.

**Data access note:** The hourly dataset is large. Download it from the official source as needed; avoid committing large raw data files to GitHub.

## Planned Methodology

1. **Dataset Inspection:** Examine structure, data types, date coverage, missing values, and duplicates.
2. **Preprocessing:** Validate timestamps and variables, address data-quality issues, and prepare analysis-ready data.
3. **Exploratory Data Analysis (EDA):** Examine consumption by hour and date, price patterns, temperature, and experimental groups.
4. **Causal Design:** Identify treatment, outcome, and relevant covariates, and verify how price signals were assigned.
5. **Causal Estimation:** Use DoubleML and suitable machine-learning nuisance models only if the data and identification assumptions justify it.
6. **Validation and Interpretation:** Assess uncertainty, robustness, and limitations.
7. **Dashboard and Communication:** Develop a Streamlit dashboard with Plotly visualizations and prepare the final report, presentation, and demonstration.

## Technology Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Analysis and Machine Learning:** Scikit-learn, DoubleML
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Interactive Dashboard:** Streamlit
- **Development Environment:** Jupyter Notebook, VS Code
- **Version Control:** Git and GitHub

## Repository Structure

```text
EconoCausal/
│
├── README.md
├── data/
│   └── README.md
│
├── notebooks/
│   ├── 01_dataset_inspection.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_causal_analysis.ipynb
│
├── src/
│
├── dashboard/
│
├── reports/
│
└── requirements.txt
```

This is a planned structure; folders and files will be added as the project progresses.

## Expected Deliverables

- Reproducible data inspection and preprocessing code.
- Exploratory analysis and visualizations.
- Documented causal analysis plan and validated estimates, if supported by the data.
- Interactive Streamlit dashboard.
- Final project report and presentation.
- Demonstration of the completed project.

## Current Progress

- [x] Selected the iFlex electricity-pricing experiment dataset.
- [x] Downloaded `experiment_days.csv` and `price_signals.csv`.
- [x] Initial project setup and repository creation.
- [ ] Inspect the selected CSV files.
- [ ] Load and prepare hourly consumption data.
- [ ] Complete EDA and document observations.
- [ ] Validate the causal design and estimate effects if appropriate.
- [ ] Build the dashboard after the mid-review.
- [ ] Complete the report, presentation, and demonstration.

## Important Note

The causal conclusions of this project depend on the experiment design, treatment assignment, data quality, and statistical assumptions. The analysis will document these checks and limitations before presenting any causal claims.

## Acknowledgment

This project uses the iFlex dataset made available through Zenodo.

Please refer to the [official dataset record](https://zenodo.org/records/8248802) for the dataset description, citation, and usage information.
