# HMDA Mortgage Denial Analysis

Loan-level logistic regression analysis of 2025 North Carolina mortgage applications, measuring how much of the raw racial gap in denial rates remains after controlling for financial factors. After the controls are accounted for, a 1.94x adjusted odds disparity remains. The financial variables only explain about a fifth of the gap. 


## Question

Group-level denial rates differ across applicant race. How much of that is explained by legitimate financial factors, and how much persists once those are controlled for? The controlled factors are income, loan to value, and debt to income ratio.

## Data

Source: 2025 Home Mortgage Disclosure Act (HMDA) data, North Carolina, from the FFIEC / CFPB public dataset (ffiec_.cfpb.gov). 
Observation: one row per mortgage application
Volume: ~513,000 records. 
Analysis universe: ~231,000 applications after exclusions.

## Methodology

### Exclusions

The raw file includes records that cannot be included for a true denial analysis. For example, withdrawn applications, incomplete files, purchased loans, and rows missing the financial fields such as income that the analysis depends on. Each is applied as an explicit step, reducing the dataset from 513k records to approximately 231k observations. 
### Staged Logistic regression

Denial is modeled as a function of applicant race, then financial controls are layered in stage by stage. Income, loan-to-value ratio (LTV) and debt-to-income (DTI). This shows how much of the raw gap between races each control absorbs, and how much is remaining at the end.


## Findings

- ~23.8% overall denial rate across decisioned applications.

- Financial controls(income, DTI, LTV) account for only ~20% of the raw Black-White denial gap.

- A 1.94x adjusted odds disparity remains after controls (95% CI 1.87-2.02)


This model quantifies an association that survives the financial controls available in the HMDA dataset. However, it does not identify the cause for the discrepancy in denial rates and should not be interpreted as evidence of discrimination alone. Credit score and underwriting detail are absent in the public data which could be large contributors. 

## Tech Stack

Python - data extract, cleaning, analysis
SQL (DuckDB) - filtering and exclusion pipeline.
statsmodels - logistic regression and confidence intervals

## Limitations and next steps

- Missing underwriting variables: HMDA omits credit score and underwriting data.

- Single state: Currently North Carolina only. Planned future work includes scaling the pipeline with dbt and a data warehouse to support multi-state analyses.


