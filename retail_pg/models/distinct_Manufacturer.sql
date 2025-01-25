-- distint manufacturers and their sellings
with CTE_view as(
select 
    manufacturer,
    count(*) as helped_in_building,
	sum(cost_in_credits) contributed_in_selling
from	
(select 
        m.manufacturer1 as manufacturer,
		f.cost_in_credits as cost_in_credits
    from public.dim_starships as s
    inner join public.fact_starships as f
        ON s.id = f.id
    inner join public.dim_manufacturers as m
        ON m.id = s.manufacturer_id

    union all
	
    select 
        m.manufacturer2 as manufacturer,
		f.cost_in_credits as cost_in_credits
    FROM public.dim_starships as s
    inner join public.fact_starships as f
        on s.id = f.id
    inner join public.dim_manufacturers as m
        on m.id = s.manufacturer_id
    where m.manufacturer2 is not null
) as combined_manufacturers
group by manufacturer
)

select * from CTE_view
where helped_in_building > 0 and contributed_in_selling > 0
order by helped_in_building desc , contributed_in_selling  desc
                     