SELECT * FROM {{ ref('stg_applications') }}
WHERE occupancy_type = 1
  AND business_or_commercial_purpose = 2
  AND reverse_mortgage = 2
  AND open_end_line_of_credit = 2
  AND total_units IN ('1','2','3','4')
  AND action_taken in (1, 2, 3)