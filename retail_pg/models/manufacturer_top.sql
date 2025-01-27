select 
    * ,
    RANK() OVER  (ORDER BY helped_in_building DESC, contributed_in_selling  desc) AS Rank  
from {{ref ('distinct_Manufacturer')}}
order by helped_in_building desc , contributed_in_selling  desc
--limit 10