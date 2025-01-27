-- Analyzes selling count, average selling price, and atmospheric speed by starship class.
with class_details_cte as 
(
    select 
        s.starship_class,
        f.cost_in_credits,
        f.max_atmosphering_speed,
        f.crew,
        f.length
    from public.dim_starships as s
    inner join public.fact_starships as f
    ON s.id = f.id
),

class_ave_cte as 
(
    select starship_class, 
    count(*) as selling_count, 
    ROUND(avg(case when cost_in_credits is not null then cost_in_credits else 0 end ),0) as avg_selling_price,
    ROUND(avg(case when max_atmosphering_speed is not null then max_atmosphering_speed else 0 end ),0) as avg_atmosphering_speed,
    (sum(case when crew is not null then crew else 0 end) / nullif(count(crew), 0)) as avg_crew_size,
    avg(length) as avg_length
    from class_details_cte
    group by starship_class
)
select * 
from class_ave_cte
where avg_selling_price <> 0 and avg_atmosphering_speed <> 0 and avg_crew_size <> 0
order by selling_count desc

