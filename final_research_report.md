# EconoCausal: Electricity Price Impact Analyzer

## 1. Executive Summary

This project, EconoCausal: Electricity Price Impact Analyzer, investigates
how experimental electricity price signals affect household electricity
consumption. The analysis uses data from the iFlex electricity pricing
experiment conducted in Norway.

The study examines two experimental phases separately. It uses hourly
household electricity consumption as the primary outcome and daily
consumption as a secondary outcome. Data preparation, exploratory analysis,
treatment-assignment validation, and causal regression methods were used.

For Phase 1, the primary Double Machine Learning specification estimated
a treatment effect of +0.0792 kWh per household-hour (p = 0.4818).
For Phase 2, the full fixed-effects regression estimated a treatment effect
of -0.0773 kWh per household-hour (p = 0.1645). The Phase 2 daily analysis
estimated a treatment effect of -1.8549 kWh per household-day
(p = 0.1645). None of these primary estimates was statistically significant
at the 5% level.

The Phase 2 hourly estimate was also virtually unchanged when temperature
was excluded from the regression specification. This provides evidence
that the estimate is stable to this particular modelling choice.

Overall, the analysis does not find statistically significant evidence
that assignment to the experimental price group changed average household
electricity consumption in either phase. This does not prove that the true
effect is zero. Differences in experimental design, group structure, and
model specifications mean that comparisons between phases should be
interpreted cautiously.

The project also identifies important limitations, including incomplete
survey coverage, regional differences in Phase 2 treatment assignment,
uncertainty about the detailed randomisation procedure, and the inability
to estimate the optional full-sample Driscoll-Kraay standard errors because
of available system memory.

## 2. Introduction and Research Question

### 2.1 Background

Electricity consumption is influenced by several factors, including
weather conditions, household characteristics, electricity prices,
and consumer behaviour. Dynamic electricity pricing is one approach
used to encourage consumers to adjust their electricity consumption
in response to changing price signals.

The iFlex project in Norway conducted an experimental electricity
pricing study in which participating households were assigned to
experimental price or control groups. The experiment provides an
opportunity to investigate how experimental price signals influence
household electricity consumption.

### 2.2 Problem Statement

Although dynamic pricing is intended to encourage households to
shift or reduce electricity consumption during selected periods,
the actual response of households may vary. It is therefore important
to evaluate the effect of experimental price-group assignment using
household-level electricity consumption data and appropriate
causal analysis methods.

### 2.3 Main Research Question

How do experimental electricity price signals affect household
electricity consumption?

### 2.4 Research Objectives

The main objectives of this project are:

1. Understand the experimental design and structure of the iFlex dataset.
2. Prepare and validate household-level hourly electricity consumption data.
3. Explore consumption patterns across households, dates, regions,
   and experimental groups.
4. Examine the relationship between experimental price-group assignment
   and household electricity consumption.
5. Estimate treatment effects separately for Phase 1 and Phase 2.
6. Conduct robustness and secondary-outcome analyses.
7. Compare findings across the two experimental phases.
8. Communicate the findings, limitations, and implications through
   a research report and interactive dashboard.

## 3. iFlex Experiment Background

### 3.1 Experiment Overview

The iFlex study was a field experiment conducted with participating
households in Norway. Households opted into the project and were
randomly assigned to either a price group or a control group.

Households in the price group were assigned to receive experimental
electricity price signals on scheduled experiment days. Control-group
households remained under normal, non-experimental pricing conditions.

The experimental price signals were additional to existing electricity
tariffs. They were designed to provide financial incentives for
households to reduce or adjust electricity consumption during
selected periods.

### 3.2 Experimental Phases

The experiment was conducted in two separate phases:

- **Phase 1:** 6 January 2020 to 20 March 2020. This phase ended
  earlier than originally planned because of the COVID-19 situation.
- **Phase 2:** 1 December 2020 to 26 March 2021.

The phases are analysed separately because their periods, group
structures, and sample sizes differ.

### 3.3 Price Signal Scheduling

Experimental price signals were scheduled for selected days and hours.
The selection of experiment days was made approximately one week
in advance using weather forecasts. Participants were notified
one day before the scheduled experiment.

This scheduling process is important when interpreting household
responses because participants could anticipate an upcoming
experimental price period after receiving the notification.

### 3.4 Treatment Assignment and Signal Receipt

This study distinguishes between treatment assignment and actual
price-signal receipt.

Treatment assignment refers to whether a household was officially
allocated to the experimental price group or the control group.
Actual signal receipt refers to whether a price signal was scheduled
for a particular household on a particular date and hour.

The main causal analysis uses official price-group assignment
to estimate the intention-to-treat (ITT) effect. This avoids
classifying households as untreated simply because they did not
receive a signal during every observed hour.

### 3.5 Experimental Design Considerations

The available experiment documentation confirms random assignment
to price and control groups. However, it does not provide enough
detail to establish the exact randomisation procedure, including
whether assignment used individual, block, or stratified
randomisation.

Phase 2 also shows differences in treatment-group proportions
across regions. These differences are considered in the analysis
and interpretation rather than being treated as proof that
randomisation failed.

## 4. Dataset and Data Preparation

### 4.1 Data Sources

The analysis uses the iFlex experimental dataset, which contains
household electricity consumption, participant information,
experiment schedules, price signals, and survey responses.

The main data files include:

- `data_hourly.csv`: hourly household electricity consumption
  and related weather and price-signal variables.
- `participants.csv`: household participation information and
  official experimental group assignments.
- `experiment_days.csv`: scheduled experimental dates and
  associated price-signal information.
- `price_signals.csv`: hourly details of the experimental
  electricity price signals.
- `survey1_answers.csv` and `survey1_questions.csv`:
  household survey responses and question descriptions.

### 4.2 Main Consumption Dataset

The hourly consumption dataset contains 13,515,600 observations
and 4,429 unique experimental households. It covers the period
from 6 January 2020 to 26 March 2021.

The observations are divided into two phases:

- Phase 1: 1,335,600 hourly observations.
- Phase 2: 12,180,000 hourly observations.

Phase 1 covers 6 January to 20 March 2020, while Phase 2 covers
1 December 2020 to 26 March 2021.

### 4.3 Treatment Assignment

Official treatment assignment was obtained from the participant
data using the `Control_Price_Phase1` and `Control_Price_Phase2`
variables.

These variables distinguish the experimental price group from
the control group. They were used instead of inferring treatment
assignment from observed price-signal receipt.

The Phase 1 causal analysis contains 742 households:
439 assigned to the price group and 303 assigned to the control group.

The Phase 2 causal analysis contains 4,375 households:
3,103 assigned to the price group and 1,272 assigned to the
control group.

### 4.4 Data Preparation and Validation

The hourly data were filtered separately for each experimental
phase and linked with participant information using household IDs.

Date and hour variables were prepared for time-based analysis.
Treatment assignment and regional information were retained for
the causal models.

The Phase 2 hourly panel contains 2,784 observations per household,
corresponding to 116 dates and 24 hours per date. The panel is
balanced across the 4,375 households.

### 4.5 Missing Values and Data Handling

Missing values in `Price_signal` and `Experiment_price_NOK_kWh`
are expected for observations outside scheduled experimental
signal periods. They were not replaced with zero because a missing
signal does not mean that a zero-price signal was received.

Zero electricity consumption observations were retained.
No negative or missing electricity consumption values were found
in the Phase 2 dataset.

### 4.6 Survey Data

Survey responses were linked to household records where available.
Survey coverage was substantially different across phases.

Phase 1 survey coverage was 701 of 742 households. Phase 2 coverage
was 654 of 4,375 households, or approximately 14.95%.

Because Phase 2 survey responses were limited and unevenly
distributed across regions and treatment groups, survey variables
were treated as exploratory information rather than required
controls in the main causal analysis.

## 5. Exploratory Data Analysis

### 5.1 Household Consumption Patterns

Exploratory analysis was conducted separately for Phase 1 and
Phase 2 to understand household electricity consumption across
time and experimental groups.

In Phase 2, the average hourly consumption was approximately
2.613 kWh for the control group and 2.544 kWh for the price group.
The descriptive difference was approximately -0.069 kWh per hour.
This is a descriptive comparison and should not be interpreted
as a causal treatment effect.

### 5.2 Treatment Assignment and Regional Differences

Phase 2 treatment assignment was examined across six regions:
Bergen, Bodø, Oslo, Stavanger, Tromsø, and Trondheim.

A chi-square test identified statistically significant differences
in treatment-group proportions across regions (p < 0.001).
Cramér's V was approximately 0.258, indicating a moderate
association between region and treatment assignment.

This result does not establish that randomisation failed.
However, it highlights the importance of accounting for regional
differences in the causal analysis.

### 5.3 Experimental Signal Validation

Observed price-signal exposure was compared with the official
experiment schedule.

For Phase 1, all 63,717 observed household-date signal records
matched the scheduled experiment information.

For Phase 2, all 60,865 unique household-date-signal records
matched the experiment schedule. No unmatched records were found.

These checks support the consistency of the observed signal
records with the documented schedules.

### 5.4 Treatment Assignment Versus Signal Exposure

Not every hour assigned to a price-group household contained
an experimental price signal. In Phase 2, 1,460,760 treatment-group
hours contained a signal, while 7,177,992 treatment-group hours
did not.

Control-group households had no observed experimental signal
hours. This distinction supports the use of official group
assignment for the main intention-to-treat analysis.

### 5.5 Household Panel Structure

The Phase 2 dataset contains 4,375 households observed over
116 dates, with 24 hourly observations per date. Each household
has 2,784 hourly observations.

The balanced panel structure supports comparisons across
households and time while accounting for repeated observations
from the same household.

### 5.6 Survey Response Coverage

Survey coverage differed considerably between phases.

In Phase 1, 701 of 742 households had survey responses,
representing approximately 94.5% coverage.

In Phase 2, only 654 of 4,375 households had survey responses,
representing approximately 14.95% coverage. Response rates
also varied substantially across regions.

Consequently, survey characteristics were not used as essential
controls in the main causal models. Survey-based findings should
be interpreted as exploratory.

### 5.7 EDA Summary

The exploratory analysis confirmed that the main consumption
panel is suitable for phase-specific analysis and that observed
price-signal records match the experiment schedules.

It also identified regional differences in Phase 2 treatment
assignment and limited survey coverage. These findings informed
the model specifications and the interpretation of the causal
results.

## 6. Research Methodology and Causal Identification

### 6.1 Empirical Strategy

The analysis estimates the effect of assignment to the experimental
electricity price group on household electricity consumption.
The primary outcome is hourly electricity consumption, measured
in kWh per household-hour.

The main analysis follows the intention-to-treat (ITT) approach.
Treatment is defined using the official experimental group
assignment rather than actual price-signal receipt.

This approach estimates the effect of being assigned to the
experimental price group, even when a household does not receive
a signal during every observed hour.

### 6.2 Separate Analysis by Experimental Phase

Phase 1 and Phase 2 were analysed separately because they differ
in experimental period, group structure, and sample size.

The Phase 1 analysis uses Double Machine Learning (DML), while
the Phase 2 analysis uses fixed-effects regression with household-
clustered standard errors.

Because the estimation methods and specifications differ,
the resulting phase estimates should not be treated as a direct
like-for-like comparison.

### 6.3 Phase 1 Model

The primary Phase 1 specification uses Double Machine Learning
to estimate the treatment effect while accounting for hourly
temperature and time-related differences.

The primary model includes temperature, date effects, and hour
effects. A second specification examines regional controls as
an alternative.

The treatment coefficient represents the estimated difference
in hourly consumption associated with assignment to the price group.

### 6.4 Phase 2 Hourly Model

The primary Phase 2 fixed-effects model is:

`Demand_kWh ~ Treatment_Assigned + Temperature | Region + Date_FE + Hour_FE`

The model includes:

- `Treatment_Assigned`: official price-group assignment.
- `Temperature`: hourly outdoor temperature.
- `Region`: regional fixed effects.
- `Date_FE`: date fixed effects.
- `Hour_FE`: hour-of-day fixed effects.

Standard errors are clustered at the household level to account
for repeated observations from the same household.

### 6.5 Robustness and Secondary Outcome

A robustness specification excludes temperature while retaining
region, date, and hour fixed effects. This checks whether the
estimated treatment effect is sensitive to including temperature.

A secondary analysis aggregates hourly consumption into daily
household consumption. The daily model includes daily temperature,
region fixed effects, date fixed effects, and household-clustered
standard errors.

Daily aggregation provides a complementary outcome, although
it may hide changes in the timing of electricity consumption
within a day.

### 6.6 Interpretation of Statistical Results

Treatment effects are interpreted using their estimated
coefficients, standard errors, confidence intervals, and
p-values.

Statistical significance is assessed at the 5% level.
A result with a p-value above 0.05 is not statistically significant
at this threshold.

A statistically insignificant estimate does not prove that
the true treatment effect is zero. It indicates that the analysis
does not provide sufficient statistical evidence to reject
the null hypothesis at the chosen significance level.

### 6.7 Identification Considerations

The causal interpretation relies on the documented random
assignment of households to experimental groups and the
appropriate handling of time and regional differences.

The detailed randomisation procedure is not fully documented
in the available materials. Regional differences in Phase 2
assignment are therefore considered when specifying and
interpreting the models.

The analysis also distinguishes assignment from actual signal
receipt and treats the two experimental phases separately.

## 7. Phase 1 Causal Analysis

### 7.1 Analysis Sample

The Phase 1 causal analysis includes 742 households:
439 assigned to the experimental price group and 303 assigned
to the control group.

The analysis uses hourly household electricity consumption
as its primary outcome.

### 7.2 Primary Double Machine Learning Result

The primary Phase 1 Double Machine Learning specification
(Model A) estimated a treatment effect of:

- Treatment effect: +0.0792 kWh per household-hour.
- Standard error: 0.1125.
- p-value: 0.4818.
- 95% confidence interval: [-0.1414, 0.2997].

The estimated coefficient is positive, but it is not statistically
significant at the 5% level. The confidence interval includes zero.

Therefore, the primary model does not provide statistically
significant evidence that assignment to the experimental price
group changed average hourly electricity consumption in Phase 1.

### 7.3 Alternative Model and Supporting Checks

An alternative DML specification (Model B), using regional
controls instead of the primary temperature-based specification,
estimated a treatment effect of +0.0368 kWh per household-hour
(p = 0.7406).

A household-level adjusted OLS model estimated a treatment
effect of +0.0525 kWh per household-hour (p = 0.6386).

Both supporting estimates were also statistically insignificant.

### 7.4 Randomisation Inference

A randomisation-inference exercise using 10,000 complete
assignment permutations produced a p-value of approximately
0.4744.

A region-stratified permutation sensitivity analysis produced
a p-value of approximately 0.4840. The stratified procedure
is a hypothetical sensitivity check because the detailed
original randomisation mechanism has not been confirmed.

### 7.5 Phase 1 Interpretation

Across the primary DML model and supporting specifications,
the estimated Phase 1 effects were not statistically significant.

The results do not establish that the true treatment effect
was zero. Rather, the available analysis does not provide
sufficient evidence to conclude that assignment to the
experimental price group changed average household electricity
consumption during Phase 1.

## 8. Phase 2 Causal Analysis

### 8.1 Hourly Consumption Results

The Phase 2 hourly analysis includes 4,375 households:
3,103 assigned to the experimental price group and 1,272
assigned to the control group. The model uses 12,180,000
hourly observations.

The primary fixed-effects regression estimated the following
treatment effect:

- Treatment effect: -0.0773 kWh per household-hour.
- Standard error: 0.0556.
- p-value: 0.1645.
- 95% confidence interval: approximately [-0.186, 0.032].

The estimated effect is negative, suggesting lower average
hourly consumption among households assigned to the price group.
However, the estimate is not statistically significant at the
5% level, and its confidence interval includes zero.

The model also includes region, date, and hour fixed effects,
hourly temperature, and standard errors clustered by household.

### 8.2 Temperature Robustness Check

A second specification excluded temperature while retaining
region, date, and hour fixed effects.

The estimated treatment coefficient remained approximately
-0.0773 kWh per household-hour, with a p-value of approximately
0.164.

The treatment estimate was virtually unchanged by excluding
temperature. This indicates stability to this particular
specification change. It does not establish robustness to
every possible modelling choice.

### 8.3 Daily Consumption Results

A secondary analysis aggregated hourly consumption into
daily household consumption. The daily dataset contains
507,500 household-day observations.

The daily fixed-effects regression estimated:

- Treatment effect: -1.8549 kWh per household-day.
- Standard error: 1.3342.
- p-value: 0.1645.
- 95% confidence interval: approximately [-4.471, 0.761].

The estimated daily effect is negative but not statistically
significant at the 5% level.

Daily aggregation provides a useful secondary perspective.
However, it may conceal changes in consumption timing within
individual days, which can be important when studying dynamic
electricity pricing.

### 8.4 Phase 2 Interpretation

The primary hourly model and secondary daily model both
produced negative treatment estimates. Neither estimate was
statistically significant at the 5% level.

Therefore, the Phase 2 results do not provide sufficient
statistical evidence that assignment to the experimental
price group changed average household electricity consumption.

These findings should be interpreted alongside the regional
differences in treatment assignment and the limitations
discussed later in this report.

### 8.1 Hourly Consumption Results

### 8.2 Temperature Robustness Check

### 8.3 Daily Consumption Results

## 9. Comparison Between Phase 1 and Phase 2

### 9.1 Primary Results

The primary hourly treatment-effect estimates from the two
experimental phases are summarised below.

| Experimental Phase | Primary Method | Treatment Effect (kWh/hour) | p-value |
|---|---|---:|---:|
| Phase 1 | Double Machine Learning, Model A | +0.0792 | 0.4818 |
| Phase 2 | Fixed-effects regression | -0.0773 | 0.1645 |

Both estimates are statistically insignificant at the 5% level.

### 9.2 Comparison of Estimated Effects

The Phase 1 estimate is positive, while the Phase 2 estimate
is negative. However, neither estimate provides statistically
significant evidence of a change in average hourly household
electricity consumption.

The difference in estimated signs should not be interpreted
as proof that household responses changed between phases.

### 9.3 Important Comparability Considerations

The phases differ in their experimental periods, sample sizes,
group structures, and estimation methods. Phase 1 uses a
Double Machine Learning specification, whereas Phase 2 uses
fixed-effects regression.

These differences limit the extent to which the coefficients
can be compared directly. A formal conclusion about changes
in treatment effects between phases would require a comparable
estimation framework and an appropriate test of the difference.

### 9.4 Overall Comparison

The main finding across both phases is that neither primary
hourly model detects a statistically significant treatment
effect at the 5% level.

The results are therefore consistent in their lack of
statistically significant evidence, even though the estimated
coefficients have opposite signs.

## 10. Discussion and Interpretation

### 10.1 Main Findings

The analysis does not find statistically significant evidence
that assignment to the experimental electricity price group
changed average household electricity consumption in either
Phase 1 or Phase 2.

The Phase 1 primary estimate was positive, while the Phase 2
primary estimate was negative. However, both estimates had
p-values above 0.05 and confidence intervals that included zero.

These results should not be interpreted as proof that
experimental price signals had no effect. They indicate that
the analysis did not establish a statistically significant
average treatment effect.

### 10.2 Understanding the Intention-to-Treat Results

The analysis estimates the effect of assignment to the
experimental price group rather than the effect of receiving
a price signal in every hour.

In Phase 2, only a proportion of treatment-group hours
contained experimental price signals. The ITT estimate
therefore reflects the effect of group assignment across
the observed study period, including hours without an
experimental signal.

This distinction is important when interpreting the size
of the estimated treatment effects.

### 10.3 Hourly and Daily Outcomes

The Phase 2 hourly and daily estimates were both negative
and statistically insignificant.

Hourly data provide detailed information about consumption
patterns, while daily aggregation measures total consumption
over a full day. Daily aggregation may conceal changes in
the timing of electricity use, even when total daily
consumption remains similar.

For this reason, hourly consumption is retained as the
primary outcome and daily consumption as a secondary outcome.

### 10.4 Model Stability

The Phase 2 hourly treatment estimate was virtually unchanged
when temperature was excluded from the model. This suggests
that the main estimate is not sensitive to this particular
temperature-control choice.

However, stability under one alternative specification
does not guarantee that the result is robust to all possible
model assumptions.

### 10.5 Overall Interpretation

Taken together, the results do not provide sufficient
statistical evidence of an average consumption response
to experimental price-group assignment in either phase.

The findings should be understood in the context of the
experimental design, regional assignment patterns, differences
between phases, and the limitations of the available data
and documentation.

## 11. Research Limitations

### 11.1 Incomplete Randomisation Documentation

The available experiment documentation confirms random assignment
to price and control groups but does not fully describe the
randomisation procedure.

Details such as individual versus stratified assignment and
the exact allocation mechanism for experimental subgroups
could not be independently confirmed. This limits the ability
to reproduce the original assignment process exactly.

### 11.2 Regional Differences in Phase 2 Assignment

Phase 2 treatment-group proportions differed across regions.
Although regional fixed effects were included in the main
regression, the observed imbalance remains an important
consideration when interpreting the results.

The regional differences alone do not demonstrate that
randomisation failed.

### 11.3 Voluntary Participation and Generalisability

Households opted into the iFlex project. Consequently,
participating households may not represent all households
in Norway.

The findings should therefore be generalised beyond the
participating sample with caution.

### 11.4 Differences Between Experimental Phases

Phase 1 and Phase 2 differed in their periods, sample sizes,
and group structures. Phase 1 also ended earlier than planned
because of the COVID-19 situation.

The two phases used different primary estimation methods,
which further limits direct comparison of their treatment
coefficients.

### 11.5 Survey Coverage

Survey coverage was high in Phase 1 but limited in Phase 2.
Only 654 of 4,375 Phase 2 households had survey responses,
and coverage varied substantially across regions.

This prevents reliable use of survey characteristics as
controls for the full Phase 2 sample. Survey-based findings
should be treated as exploratory.

### 11.6 Scheduling and Anticipation

Experiment days were selected approximately one week ahead
using weather forecasts, and participants were notified
one day before the scheduled experiment.

This scheduling and notification process may influence
household behaviour before or during experimental periods.
The present analysis does not separately identify all
possible anticipation effects.

### 11.7 Statistical and Computational Limitations

The optional full-sample Driscoll-Kraay standard-error
sensitivity analysis could not be completed because of
available system memory.

The main Phase 2 model instead uses household-clustered
standard errors. The inability to estimate the optional
Driscoll-Kraay specification limits the range of inference
checks available.

### 11.8 Interpretation of Insignificant Results

The primary treatment estimates in both phases were not
statistically significant at the 5% level.

A lack of statistical significance does not establish that
the true effect is zero. The estimates should be interpreted
alongside their confidence intervals, sample structure,
and modelling assumptions.

## 12. Conclusion

This project investigated how experimental electricity price
signals affect household electricity consumption using data
from the iFlex field experiment in Norway.

The analysis examined Phase 1 and Phase 2 separately, using
hourly household electricity consumption as the primary
outcome and daily consumption as a secondary outcome.

For Phase 1, the primary Double Machine Learning model
estimated a treatment effect of +0.0792 kWh per household-hour
(p = 0.4818).

For Phase 2, the primary fixed-effects regression estimated
a treatment effect of -0.0773 kWh per household-hour
(p = 0.1645). The secondary daily model estimated
-1.8549 kWh per household-day (p = 0.1645).

None of these primary estimates was statistically significant
at the 5% level. Therefore, the analysis does not find
sufficient statistical evidence that assignment to the
experimental price group changed average household electricity
consumption in either phase.

This conclusion does not mean that the true effect was zero.
The results must be interpreted in light of the experimental
design, regional assignment differences, survey coverage,
and methodological limitations.

Overall, the project demonstrates how household-level
electricity data, exploratory analysis, and causal inference
methods can be combined to investigate the impact of
experimental electricity pricing.

## 13. References

### 13.1 Primary Research Publication

Hofmann, M., & Siebenbrunner, C. (2023).
iFlex electricity consumption and experimental pricing dataset.
*Data in Brief*.

https://doi.org/10.1016/j.dib.2023.109571

### 13.2 Experimental Dataset

iFlex experimental dataset. Zenodo repository.

https://zenodo.org/records/8248802

### 13.3 Project Documentation

The following project documents were used to guide the
experimental interpretation and analysis:

- `reports/experiment_documentation.md`
- `reports/research_methodology.md`
- `reports/research_sources.md`
- `reports/eda_report.md`

### 13.4 Software and Analytical Tools

The project used Python and the following analytical tools:

- Python 3.12.10
- pandas and NumPy for data preparation and numerical analysis.
- Matplotlib and Seaborn for exploratory visualisation.
- DoubleML for Double Machine Learning analysis.
- pyfixest for fixed-effects regression.
- Jupyter Notebook for interactive analysis.
- Streamlit and Plotly for dashboard development.
