-- buiulding an OBT for all records
-- the model fills missing values using simple maths according to each starship model
-- sometimes we add data based on domain knowledge of the starships. 
-- filling missing data is important for later ML implementation (not implemented yet)
-- i try to group the starships based on arbitratry data. I will check the groups with the results of the ML later. 
-- results is saved as a table. 

{{ config(
    materialized="table",
) }}

with joined_starship_cte as
(
    select * 
    from public.dim_starships as ds
    inner join public.fact_starships as fs
    on ds.id = fs.id
),

class_stats AS (
    SELECT
        starship_class,
        -- Get class averages for speed and length
        AVG(max_atmosphering_speed) AS class_avg_speed,
        AVG(length) AS class_avg_length,
		-- Get median for missing costs
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cost_in_credits) AS class_median_cost
    FROM joined_starship_cte
    GROUP BY starship_class
),

starship_details_cte AS (
    SELECT
        ds.id AS starship_id,
        ds.name AS starship_name,
        ds.starship_class,
        ds.manufacturer_id,
        dm.manufacturer1,
        dm.manufacturer2,
        -- replace missing cost with class median
        COALESCE(
            fs.cost_in_credits, 
            cs.class_median_cost
        ) AS cost_in_credits,
        -- replace missing crew with 0 
        COALESCE(fs.crew, 0) AS crew,
        -- replace missing passengers with 0
        COALESCE(fs.passengers, 0) AS passengers,
        -- replace speed with starship class average. in case no average for class then get global avg
        COALESCE(
            fs.max_atmosphering_speed, 
            cs.class_avg_speed, 
            (SELECT AVG(max_atmosphering_speed) FROM public.fact_starships)
        ) AS max_atmosphering_speed,
        -- replace length with class average
        COALESCE(
            fs.length, 
            cs.class_avg_length,
            CASE  --  i asked chatgpt to help me with this classification. 
                WHEN ds.starship_class = 'Starfighter' THEN 12.5
                WHEN ds.starship_class LIKE '%Freighter%' THEN 150.0
                ELSE 50.0
            END
        ) AS length
        
    FROM public.dim_starships AS ds
    INNER JOIN public.fact_starships AS fs
        ON ds.id = fs.id
    INNER JOIN public.dim_manufacturers AS dm
        ON ds.manufacturer_id = dm.id
    LEFT JOIN class_stats AS cs
        ON ds.starship_class = cs.starship_class
)

SELECT
    starship_id,
    starship_name,
    starship_class,
    manufacturer1,
    manufacturer2,
    cost_in_credits,
    crew,
    passengers,
    max_atmosphering_speed,
    length,
    CASE -- i tried to make an arbitrary classification . these values are my own. no science behinde them. 
        WHEN (crew <= 10 AND cost_in_credits <= 1000000) OR (length <= 100 AND cost_in_credits <= 1000000) THEN 'small starships'
        WHEN (crew > 10 AND crew <= 100 AND cost_in_credits > 1000000 AND cost_in_credits <= 100000000) OR (length > 100 AND length <= 1000 AND cost_in_credits > 1000000 AND cost_in_credits <= 100000000) THEN 'medium starships'
        WHEN (crew > 100 AND cost_in_credits > 100000000) OR (length > 1000 AND cost_in_credits > 100000000) THEN 'large starships'
    END AS starship_group,
    CASE
        WHEN max_atmosphering_speed >= (2000 * 0.75) THEN 'high speed'
        WHEN (max_atmosphering_speed >= (2000 * 0.5)) AND (max_atmosphering_speed < (2000 * 0.75)) THEN 'medium speed'
        WHEN (max_atmosphering_speed < (2000 * 0.5)) THEN 'low speed'
    END AS speed_classification
FROM starship_details_cte
