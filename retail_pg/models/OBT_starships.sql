{{ config(
    materialized="table",
) }}
with starship_details_cte as (
    SELECT
        ds.id as starship_id,
        ds.name as starship_name,
        ds.starship_class,
        ds.manufacturer_id,
        dm.manufacturer1,
        dm.manufacturer2,
        fs.cost_in_credits,
        fs.crew,
        fs.passengers,
        fs.max_atmosphering_speed,
        fs.length
    from
        public.dim_starships as ds
    inner join 
        public.fact_starships as fs
        ON ds.id = fs.id
    inner join 
        public.dim_manufacturers as dm
        ON ds.manufacturer_id = dm.id
)

select
    starship_id,
    starship_name,
    starship_class,
    manufacturer1,
    manufacturer2,
    cost_in_credits,
    crew,
    passengers,
    max_atmosphering_speed,
    length,
    case
        when (crew <= 10 and cost_in_credits <= 1000000) OR (length <= 100 and cost_in_credits <= 1000000) then 'small starships'
        when (crew > 10 and crew <= 100 and cost_in_credits > 1000000 and cost_in_credits <= 100000000) OR (length > 100 and length <= 1000 and cost_in_credits > 1000000 and cost_in_credits <= 100000000) then 'medium starships'
        when (crew > 100 and cost_in_credits > 100000000) OR (length > 1000 and cost_in_credits > 100000000) then 'large starships'
    end as starship_group,
    case
        when max_atmosphering_speed >= (2000 * 0.75) then 'high speed'
        when (max_atmosphering_speed >= (2000 * 0.5)) and (max_atmosphering_speed < (2000 * 0.75)) then 'medium speed'
        when (max_atmosphering_speed < (2000 * 0.5)) then 'low speed'
    end as speed_classification
from
    starship_details_cte