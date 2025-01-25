--Analyzes manufacturers, their selling count, and the diversity of manufactured classes.
WITH manufacturer_details_cte AS (
    SELECT 
        m.id as manufacturer_id,
        s.starship_class,
        m.manufacturer1,
		COALESCE(m.manufacturer2, 'N/A') AS manufacturer2,
		f.cost_in_credits
    FROM public.dim_starships AS s
    INNER JOIN public.fact_starships AS f
    ON s.id = f.id
    INNER JOIN public.dim_manufacturers AS m
    ON m.id = s.manufacturer_id
)

select 
    manufacturer1, manufacturer2, 
    count(*) as selling_count, 
    count(DISTINCT starship_class) as manufactured_classes,
	sum(cost_in_credits) as total_revenue,
	round(avg(cost_in_credits),0) as avg_cost_for_ship
from manufacturer_details_cte as m
group by m.manufacturer1,manufacturer2, manufacturer_id
order by selling_count desc
--LIMIT 5;