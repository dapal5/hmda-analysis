SELECT *
FROM {{ ref('int_universe') }}
WHERE (action_taken = '3' AND denied != 1)
   OR (action_taken != '3' AND denied != 0)
