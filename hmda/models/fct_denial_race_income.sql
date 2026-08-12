SELECT
    derived_race,
    CASE
        WHEN income IS NULL THEN 'e: not reported'
        WHEN income < 50  THEN 'a: <50k'
        WHEN income < 100 THEN 'b: 50-100k'
        WHEN income < 150 THEN 'c: 100-150k'
        ELSE 'd: 150k+'
    END AS income_band,
    COUNT(*) AS total,
    SUM(denied) AS denials,
    SUM(denied) * 1.0 / COUNT(*) AS denial_rate
FROM {{ ref('int_universe') }}
WHERE derived_race IN ('White', 'Black or African American', 'Asian')
GROUP BY derived_race, income_band
ORDER BY income_band, derived_race