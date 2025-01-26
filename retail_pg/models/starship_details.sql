--Provides key product details for each starships.
select 
    ds.name as starship_name,
    ds.starship_class,
    fs.cost_in_credits,
    fs.crew,
    fs.passengers
from fact_starships as fs
join dim_starships as ds
on fs.id = ds.id
order by cost_in_credits IS NULL, cost_in_credits DESC
	
