-- preprocessing data and exporting to csv
{{
  config(
    materialized='table'
  )
}}

SELECT
    starship_id,
    starship_name,
    cost_in_credits,
    crew,
    passengers,
    max_atmosphering_speed,
    length,
    starship_group as starship_group_manually
FROM
    {{ ref('OBT_starships') }}
where cost_in_credits <> 0 

