# EconoCausal: Research Methodology

## 1. Research Background

Electricity prices can influence household decisions about electricity consumption. Dynamic electricity pricing experiments provide an opportunity to investigate how households respond to different price signals.

This project aims to study the relationship between experimental electricity price signals and household electricity consumption.

## 2. Problem Statement

Understanding how households respond to electricity price changes is important for evaluating dynamic electricity pricing strategies.

However, changes in electricity consumption may also be influenced by factors other than price, such as weather, time of day, household characteristics and seasonal patterns.

Therefore, simply observing a relationship between electricity prices and consumption may not establish a causal effect.

## 3. Main Research Question

How do experimental electricity price signals affect household electricity consumption?

## 4. Research Objectives

1. Understand the electricity pricing experiment and its design.
2. Examine electricity price signals and household consumption patterns.
3. Identify relevant treatment, outcome and control variables.
4. Investigate whether the experiment supports causal inference.
5. Explore Double Machine Learning as a potential estimation method.
6. Present the findings through an interactive dashboard.

## 5. Proposed Methodology

The project will follow these stages:

### 5.1 Experiment Understanding

Study the experiment documentation, participant groups, price signals, assignment mechanism and experiment timeline.

### 5.2 Data Preparation

Inspect the available datasets, identify missing values, examine data quality and prepare the data for analysis.

### 5.3 Exploratory Data Analysis

Explore electricity prices and consumption patterns using descriptive statistics and visualizations.

### 5.4 Causal Inference

Evaluate whether the experimental design supports estimating the causal effect of electricity price signals on household electricity consumption.

### 5.5 Double Machine Learning

Consider Double Machine Learning (DoubleML) if the treatment definition, outcome data, assignment mechanism and available observations support an appropriate estimator.

## 6. Key Research Variables

The following variables are proposed and will be finalized after examining the dataset:

- Treatment: Electricity price signal or assigned pricing condition.
- Outcome: Household electricity consumption.
- Potential control variables: Weather, time-related variables and household characteristics, depending on availability.

## 7. Proposed Technology Stack

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- DoubleML
- Jupyter Notebook
- Streamlit
- Plotly

## 8. Research Limitations

Potential limitations include:

- Availability and quality of household consumption data.
- Differences between participant groups.
- Missing observations.
- Other factors influencing electricity consumption.
- Limitations in the experimental assignment design.
- Whether the available data supports the selected causal inference method.

## 9. Expected Outcome

The expected outcome is a research-based analysis of how experimental electricity price signals influence household electricity consumption, supported by an interactive dashboard.

Actual causal conclusions will only be reported if supported by the experiment design and empirical analysis.

## 10. Current Status

Initial project setup and introductory documentation have been completed.

Experiment investigation, data preparation, statistical analysis and causal estimation are pending.