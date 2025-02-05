
WITH starship_clusters_cte AS (  
    SELECT 
        starship_class,
        CASE 
            WHEN cluster = 0 THEN 'small starships'  
            WHEN cluster = 1 THEN 'medium starships'
            WHEN cluster = 2 THEN 'large starships'
        END AS ml_starship_group
    FROM public.starship_clusters
),
smc_starships_cte AS (
    SELECT
        starship_class,
        starship_group AS manual_starship_group  
    FROM public.starship_model_classification as smc
)
SELECT
    cl.starship_class,
    smc.manual_starship_group,
    cl.ml_starship_group
FROM starship_clusters_cte AS cl 
LEFT JOIN smc_starships_cte AS smc
ON smc.starship_class = cl.starship_class;