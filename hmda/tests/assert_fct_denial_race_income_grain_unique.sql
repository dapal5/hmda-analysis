SELECT derived_race, income_band, COUNT(*) AS n
FROM {{ ref('fct_denial_race_income') }}
GROUP BY derived_race, income_band
HAVING COUNT(*) > 1
