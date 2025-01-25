select * from {{ref ('distinct_Manufacturer')}}
order by helped_in_building desc , contributed_in_selling  desc
limit 10