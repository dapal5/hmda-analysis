{% docs stg_applications %}
**Purpose:** Thin passthrough layer over the raw HMDA LAR extract. Casts numeric fields
(`loan_amount`, `interest_rate`, `loan_to_value_ratio`, `income`, `property_value`) from the
all-VARCHAR raw source to `DOUBLE`, and renames a handful of raw columns whose names contain
hyphens (`applicant_ethnicity-1`, `applicant_race-1`, `denial_reason-1..4`,
`open-end_line_of_credit`) so they're valid unquoted SQL identifiers downstream.

**Grain:** One row per raw LAR record, 1:1 with the `raw` source table. No filtering happens
here — every row in `raw` has a corresponding row in `stg_applications`.

**Transformations:** `TRY_CAST` on the numeric fields (returns NULL rather than erroring on
malformed values, since HMDA sometimes uses non-numeric sentinel strings like `'NA'` or
`'Exempt'` in fields that are otherwise numeric). All other columns pass through unchanged.

**Assumptions:** None yet — this model exists to validate that the *raw* data matches the
domain we expect (see its tests) before any business logic is applied. If CFPB changes a
code list or the extract format shifts, it should surface here first.
{% enddocs %}

{% docs int_universe %}
**Purpose:** Defines the broad analytical universe for denial-rate analysis: mortgage
applications where a credit decision was actually made, on the loan types HMDA denial
analysis conventionally covers. This is the population referenced throughout the README's
"Analytical universe" section.

**Grain:** One row per application that survives the filter, same conceptual grain as
`stg_applications` (one row per LAR record) but restricted to a subset of rows.

**Transformations:** Adds `denied` (1 if `action_taken = '3'`, else 0). Applies the exclusion
filters described below via `WHERE`.

**Assumptions — this is the core of the analytical universe definition:**
- `occupancy_type = '1'` — principal residence only (excludes second homes and investment
  properties, which have systematically different underwriting).
- `business_or_commercial_purpose = '2'` — excludes business-purpose loans; this is a
  consumer mortgage analysis.
- `reverse_mortgage = '2'` — excludes reverse mortgages, which aren't denied/approved on the
  same basis as forward mortgages.
- `open_end_line_of_credit = '2'` — excludes HELOCs, which have a different application and
  decisioning process than closed-end mortgages.
- `total_units IN ('1','2','3','4')` — excludes 5+ unit multifamily properties, which are
  typically commercial-style underwriting.
- `action_taken IN ('1','2','3')` — keeps only applications with a real credit decision
  (originated, approved-but-not-accepted, denied). Excludes withdrawn applications (`'4'`),
  files closed for incompleteness (`'5'`), purchased loans (`'6'`, since the purchasing
  institution didn't make the origination decision), and preapproval-only actions (`'7'`,`'8'`).
- `age != '8888'` — `'8888'` is HMDA's sentinel for "age not applicable," not a real value.

**Known limitation:** the public HMDA LAR extract has no unique application identifier
(it's redacted for privacy), so there is no natural key to run a `unique` test against at
this grain. Row-count and category-level tests are used instead to validate the filtering
logic did what it's supposed to.
{% enddocs %}

{% docs int_regression_sample %}
**Purpose:** Narrows `int_universe` down to the exact complete-case sample used by the
logistic regression in `analysis/denial_model.py`. This used to be done ad hoc in pandas;
it's formalized here so the assumptions behind the regression sample are dbt-tested rather
than buried in a Python script.

**Grain:** One row per application, same as `int_universe`, restricted further.

**Assumptions — each one exists for a specific modeling reason:**
- `derived_race IN ('White','Black or African American','Asian')` — the three groups large
  enough in this dataset to estimate a reasonably precise odds ratio against; other race
  categories either have very small counts or represent an unclear mix ("Joint," "2 or more
  minority races," "Race Not Available") that shouldn't be pooled with a specific group.
- `IS NOT NULL` on every modeled column — logistic regression needs complete cases; a row
  with a missing income or DTI can't be scored by the model. This is a "used in this specific
  model" restriction, not a claim those applications are unusual.
- `loan_to_value_ratio <= 120` — caps a small number of extreme/likely-erroneous LTV values
  (loans exceeding 120% of property value are rare edge cases, not representative of normal
  underwriting) so they don't distort the coefficient.
- `income > 0` and `loan_amount > 0` — excludes non-positive values that can't be meaningfully
  logged (the model uses `np.log(income)` and `np.log(loan_amount)`) and are almost certainly
  data errors rather than real applications.
{% enddocs %}

{% docs fct_denial_by_dimension %}
**Purpose:** Simple denial-rate rollup of `int_universe` across three demographic dimensions
(race, sex, age band), one at a time. This is the "raw disparity" starting point of the
progressive analysis described in the README — before any stratification or regression.

**Grain:** One row per `(dimension, dimension_value)` pair, e.g. `('derived_race', 'Asian')`.
The three dimensions are unioned into one long/tidy table rather than three separate wide
tables, so downstream consumers (plots, the README's results tables) can filter on
`dimension` instead of picking a different table per demographic cut.

**Transformations:** `COUNT(*)`, `SUM(denied)`, and `SUM(denied)/COUNT(*)` grouped by each
dimension column in turn, unioned together.
{% enddocs %}

{% docs fct_denial_race_income %}
**Purpose:** Denial rate by race, stratified by income band — the first cut of the
progressive analysis that goes beyond a single raw disparity number, showing whether the
race gap in denial rates persists (or narrows) within similar income bands.

**Grain:** One row per `(derived_race, income_band)` pair.

**Transformations:** Buckets `income` into five bands (`<50k`, `50-100k`, `100-150k`, `150k+`,
and `not reported`), then computes `COUNT(*)`, `SUM(denied)`, and the denial rate per
`(race, income_band)` cell. Restricted to the same three races as `int_regression_sample`
for consistency with the regression results it's meant to be compared against.
{% enddocs %}
