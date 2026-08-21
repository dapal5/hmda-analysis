SELECT
    denied,
    derived_race,
    derived_sex,
    age,
    income,
    loan_amount,
    loan_to_value_ratio,
    debt_to_income_ratio,
    loan_purpose,
    lien_status
FROM {{ ref('int_universe') }}
WHERE derived_race IN ('White', 'Black or African American', 'Asian')
  AND denied IS NOT NULL
  AND derived_sex IS NOT NULL
  AND age IS NOT NULL
  AND income IS NOT NULL
  AND loan_amount IS NOT NULL
  AND loan_to_value_ratio IS NOT NULL
  AND debt_to_income_ratio IS NOT NULL
  AND loan_purpose IS NOT NULL
  AND lien_status IS NOT NULL
  AND loan_to_value_ratio <= 120
  AND income > 0
  AND loan_amount > 0
