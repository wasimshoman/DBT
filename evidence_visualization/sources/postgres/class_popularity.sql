WITH class_details_cte AS (
    SELECT 
        ds.starship_class,
        COUNT(*) AS selling_count,
        fs.created::DATE AS creation_date
    FROM dim_starships ds
    JOIN fact_starships fs ON ds.id = fs.id
    GROUP BY ds.starship_class, fs.created::DATE
)
SELECT 
    starship_class,
    creation_date,
    SUM(selling_count) OVER (PARTITION BY starship_class ORDER BY creation_date) AS cumulative_selling_count
FROM class_details_cte
ORDER BY creation_date, starship_class;
