--prepare a table to the ML script
{{
  config(
    materialized='table',
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
WHERE cost_in_credits <> 0