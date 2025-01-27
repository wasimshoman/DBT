---General aggregation metrics for each starship group
--the grouping happened with arbitrarry values
--refer to starship_model_classification model for more details
SELECT
    starship_group,
    COUNT(*) AS total_starships,
    AVG(cost_in_credits) AS avg_cost,
    AVG(max_atmosphering_speed) AS avg_speed
from 
    {{ ref('OBT_starships') }}
group by  starship_group
order by  total_starships DESC