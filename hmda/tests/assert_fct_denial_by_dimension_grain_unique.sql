SELECT dimension, dimension_value, COUNT(*) AS n
FROM {{ ref('fct_denial_by_dimension') }}
GROUP BY dimension, dimension_value
HAVING COUNT(*) > 1
