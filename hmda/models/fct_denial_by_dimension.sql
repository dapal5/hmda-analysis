SELECT 'derived_race' AS dimension, derived_race::VARCHAR AS dimension_value,
       COUNT(*) AS total, SUM(denied) AS denials, SUM(denied)*1.0/COUNT(*) AS denial_rate
FROM {{ ref('int_universe') }}
GROUP BY derived_race

UNION ALL

SELECT 'derived_sex', derived_sex::VARCHAR,
       COUNT(*), SUM(denied), SUM(denied)*1.0/COUNT(*)
FROM {{ ref('int_universe') }}
GROUP BY derived_sex

UNION ALL

SELECT 'age', age::VARCHAR,
       COUNT(*), SUM(denied), SUM(denied)*1.0/COUNT(*)
FROM {{ ref('int_universe') }}
GROUP BY age