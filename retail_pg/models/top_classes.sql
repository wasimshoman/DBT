--Identifies the top 5 selling starship classes
SELECT * FROM {{ ref('class_details')}}
limit 5