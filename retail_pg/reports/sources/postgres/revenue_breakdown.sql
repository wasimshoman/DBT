SELECT 
    dm.manufacturer,
    ds.starship_class,
    SUM(fs.cost_in_credits) AS total_revenue
FROM fact_starships fs
JOIN dim_starships ds ON fs.id = ds.id
JOIN dim_manufacturers dm ON ds.manufacturer_id = dm.id
WHERE fs.cost_in_credits IS NOT NULL
GROUP BY dm.manufacturer, ds.starship_class
ORDER BY total_revenue DESC
LIMIT 10;
