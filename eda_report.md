# EconoCausal – Exploratory Data Analysis Report

## 1. Introduction

This report documents the initial exploratory analysis of the iFlex electricity pricing experiment datasets.

## 2. Datasets Inspected

### Experiment Days
- Rows: 267
- Columns: 4
- Date range: 11 February 2020 to 25 March 2021
- Unique price signals: 14
- Unique participant groups: 13

### Price Signals
- Rows: 336
- Columns: 5
- Unique price signals: 14
- Hourly records per signal: 24

## 3. Data Quality Assessment

Both datasets were inspected for missing values and duplicate records.

| Check | Experiment Days | Price Signals |
|---|---:|---:|
| Missing values | 0 | 0 |
| Duplicate rows | 0 | 0 |

The date column was converted to datetime format for future time-based analysis.

## 4. Experiment Phase Distribution

- Phase 1: 13 experiment-day records.
- Phase 2: 254 experiment-day records.

Phase 2 contributes the majority of the experiment-day records.

## 5. Price Signal Distribution

The most frequently recorded signals were:

- B_10: 40
- B_2: 35
- P_10: 30
- B_5: 30
- B_15: 28

The least frequently recorded signals were P0_2 and P0_30, with 5 records each.

## 6. Price Profile Analysis

Average experimental prices by profile:

| Profile | Average Price (NOK/kWh) |
|---|---:|
| A | 4.16 |
| B | 5.08 |
| C | 3.95 |
| P | 1.62 |
| P0 | 1.17 |

Profile B had the highest average price, while P0 had the lowest average price.

The highest individual price observed was 30.15 NOK/kWh for signal P0_30.

## 7. Visualizations

Two initial visualizations were generated:

1. Experiment days by participation phase.
2. Average experimental electricity price by profile.

## 8. Initial Findings

- Both smaller datasets contain no missing values or exact duplicate rows.
- Fourteen different experimental price signals are represented.
- Each signal contains 24 hourly price records.
- Phase 2 contributes substantially more experiment-day records than Phase 1.
- Experimental price profiles have different average and maximum prices.

## 9. Limitations

This initial analysis covers only the experiment-day and price-signal datasets.

Household electricity consumption has not yet been inspected. Therefore, no conclusions about household consumption responses or causal effects can be drawn.

## 10. Next Steps

- Inspect the hourly household consumption dataset.
- Understand its columns, size and structure.
- Examine missing values and data quality.
- Connect consumption records with experiment dates and price signals where appropriate.
- Continue exploratory analysis.