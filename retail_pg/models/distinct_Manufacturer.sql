-- distint manufacturers and their sellings
with CTE_view as(
select 
    manufacturer,
    count(*) as helped_in_building,
	sum(cost_in_credits) contributed_in_selling
from	
(
select 
        manufacturer1 as manufacturer,
		total_revenue as cost_in_credits
from {{ ref('manufacturer_sellings')}}

union all

select 
        manufacturer2 as manufacturer,
		total_revenue as cost_in_credits
from public.manufacturer_sellings
where manufacturer2 <> 'N/A'
) as combined_manufacturers
group by manufacturer
)

select * 
from CTE_view
where helped_in_building > 0 and contributed_in_selling > 0 
order by helped_in_building desc , contributed_in_selling  desc
                     