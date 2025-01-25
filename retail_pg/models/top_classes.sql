--Identifies the top 5 selling starship classes
with class_details_cte as (
select * from public.dim_starships as s
inner join public.fact_starships as f
on s.id	= f.id
), 
class_sums_cte as (
select starship_class, count(*) as selling_count, SUM(cost_in_credits) as total_revenue
from class_details_cte
group by starship_class
)
select * from class_sums_cte
where selling_count <> 0 and total_revenue <> 0
order by selling_count desc

limit 5