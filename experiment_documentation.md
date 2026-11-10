# EconoCausal: Electricity Pricing Experiment Documentation

## 1. Introduction

The iFlex experiment was a field experiment conducted in Norway to investigate whether and how households change their electricity consumption in response to variable hourly electricity prices.

The experiment covered two winter periods from early 2020 to spring 2021.

## 2. Original Research Publication

- Authors: Matthias Hofmann and Turid Siebenbrunner
- Publication year: 2023
- Journal: Data in Brief
- Article title: A rich dataset of hourly residential electricity consumption data and survey answers from the iFlex dynamic pricing experiment
- DOI: https://doi.org/10.1016/j.dib.2023.109571

## 3. Experiment Overview

- Country: Norway
- Experiment type: Randomized controlled field experiment
- Study period: Two winter periods between 2020 and 2021
- Regions: Several Norwegian regions
- Main research interest: Household responses to variable hourly electricity prices.
- Number of tested price signals: 14

## 4. Experimental Design

Households opted into the project and were randomly assigned to treatment or control groups.

Treatment groups received different experimental electricity price signals. Control groups did not receive these experimental price signals.

The experimental price signals were additional to households' existing electricity tariffs. They did not replace the normal electricity contracts or grid tariffs.

Households could earn monetary rewards if they reduced or adjusted their electricity consumption in response to the price signals.

## 5. Experiment Phases

The experiment consisted of two phases:

### Phase 1

- Period: 6 January 2020 to 20 March 2020.
- The experiment was stopped early due to the COVID-19 pandemic.
- The published dataset reports 742 households with consumption data.

### Phase 2

- Period: 1 December 2020 to 26 March 2021.
- The published dataset reports 4,375 households with consumption data.

These household counts refer to the consumption data summarized in the research article.

## 6. Price Signals

The experiment tested 14 different price signals.

The signal identifiers include:

- A_5, A_10
- B_2, B_5, B_10, B_15
- C
- P_2, P_5, P_10, P_15
- P0_2, P0_10, P0_30

Each price signal contains 24 hourly prices representing one day.

The price profiles and peak price levels differ across signals.

## 7. How Experiment Days Were Selected

Price signals were activated on selected experiment days during winter.

The experiment days were selected approximately one week in advance using weather forecasts to identify colder days.

Treatment households were informed about an upcoming experiment day one day before it occurred.

## 8. Economic Incentive

Households could receive a monetary reward based on their electricity consumption response to the experimental price signal.

The researchers calculated a baseline using average consumption for the same hour across the previous ten eligible non-experiment days, excluding weekends and holidays.

The baseline was adjusted for weekday differences and outdoor temperature.

## 9. Important Research Variables

Potential variables for our project include:

- Household identifier
- Date and hour
- Participation phase
- Participant group
- Price signal
- Experimental electricity price
- Household electricity consumption
- Outdoor temperature

Final variable definitions will be confirmed after inspecting the actual data.

## 10. Causal Inference Considerations

The randomized treatment and control group design provides a promising foundation for causal analysis.

However, before selecting an estimator, we must investigate:

- The actual treatment assignment mechanism.
- Differences between the two experiment phases.
- The treatment and comparison conditions.
- Household-level repeated observations.
- Missing consumption observations.
- Relevant confounding and time-related factors.
- Whether treatment effects differ across households or price signals.

Double Machine Learning will be considered only after these questions are investigated.

## 11. Research Limitations

Potential limitations include:

- The first experiment phase was stopped early because of COVID-19.
- Some households have incomplete consumption records.
- Participant withdrawal and technical data issues affected data availability.
- The study took place in Norwegian regions during winter periods, which may limit generalization to other settings.

## 12. Sources

1. Hofmann, M. and Siebenbrunner, T. (2023). A rich dataset of hourly residential electricity consumption data and survey answers from the iFlex dynamic pricing experiment. Data in Brief, 50, 109571.
   https://doi.org/10.1016/j.dib.2023.109571

2. Original dataset on Zenodo:
   https://zenodo.org/records/8248802

## 13. Current Status

The original research publication and experiment overview have been reviewed.

Detailed investigation of the assignment mechanism, dataset structure and causal identification strategy is still pending.