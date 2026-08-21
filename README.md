# HMDA Mortgage Denial Analysis

## Project Overview

This project measures how much of the gap in mortgage denial rates between racial groups in North Carolina can be explained by legitimate financial factors, and how much cannot. Raw loan-level records are pulled from the federal government's public HMDA dataset, loaded into DuckDB, cleaned and modeled with dbt, and analyzed with a staged logistic regression in Python.

Group-level denial rates differ by race. Some of that gap is explained by income, how large the loan is relative to the home's value, and how much debt the applicant already carries. This project asks: after accounting for those financial factors, how much of the denial gap remains?

The headline result: even after controlling for income, loan-to-value ratio, and debt-to-income ratio, Black applicants remain about 1.99 times as likely to be denied as White applicants with similar financial profiles. Those financial controls only explain about 23% of the raw gap.

## Why This Project

Mortgage lending and mortgage analysis are common industries where I live, and it's a field I have a personal connection to. My father worked in mortgage analysis, and he helped point me toward what actually matters when looking at loan-level data: which financial variables lenders weigh, what "denial" really captures, and where public data like this does and does not tell the full story.

That connection is why I held this project to a higher standard: a correct pipeline, clearly explained exclusions, and honesty about what the regression can and cannot prove.

## Data

Source: 2025 Home Mortgage Disclosure Act (HMDA) data, North Carolina, from the FFIEC / CFPB public dataset (ffiec.cfpb.gov).
Observation: one row per mortgage application.
Volume: 552,230 records as of this pipeline run (CFPB revises the public extract periodically, so re-running the pipeline will produce a slightly different count).
Analysis universe: 252,845 decisioned applications after exclusions. The regression itself uses a further-narrowed, complete-case sample of 176,366 applications (see Methodology).

## Methodology

### Exclusions

The raw file includes records that cannot be included for a true denial analysis. For example, withdrawn applications, incomplete files, purchased loans, and rows missing the financial fields such as income that the analysis depends on. Each is applied as an explicit step, reducing the dataset from 552,230 records to 252,845 decisioned applications.

### Staged Logistic Regression

Denial is modeled as a function of applicant race, then financial controls are layered in stage by stage: income, loan-to-value ratio (LTV), and debt-to-income ratio (DTI). This shows how much of the raw gap between races each control absorbs, and how much is remaining at the end.

## Findings

- 19.3% overall denial rate across decisioned applications.

- Financial controls (income, DTI, LTV) account for only ~23% of the raw Black-White denial gap.

- A 1.993x adjusted odds disparity remains after controls (95% CI 1.922-2.065).

This model quantifies an association that survives the financial controls available in the HMDA dataset. However, it does not identify the cause for the discrepancy in denial rates and should not be interpreted as evidence of discrimination alone. Credit score and underwriting detail are absent in the public data, which could be large contributors to the gap.

## Tech Stack

- Python - data extract, cleaning, analysis
- SQL (DuckDB) - filtering and exclusion pipeline
- statsmodels - logistic regression and confidence intervals

## Limitations and next steps

- Missing underwriting variables: HMDA omits credit score and underwriting data.

- Single state: Currently North Carolina only. Planned future work includes scaling the pipeline with dbt and a data warehouse to support multi-state analyses.
