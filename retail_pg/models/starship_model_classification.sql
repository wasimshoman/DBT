-- manually classify starship models according to features. the classification is based on the following features:
-- crew, length, cost of unit in credits, atmosheric speed

with cte_view as (
    select 
        starship_class,
        avg_selling_price as avg_cost_in_credits,
        avg_atmosphering_speed as avg_max_atmosphering_speed,
        avg_crew_size as avg_crew,
        avg_length
    from {{ ref('class_details')}}
),

cte_grouped as (
select 
    starship_class,
    avg_cost_in_credits,
    avg_max_atmosphering_speed,
    avg_crew,
    avg_length,
    case
        when (avg_crew <= 10 and avg_cost_in_credits <= 1000000) or 
        (avg_length <= 100 and avg_cost_in_credits <= 1000000) then 'small starships'
        when (avg_crew > 10 and avg_crew <= 100 and avg_cost_in_credits > 1000000 and avg_cost_in_credits <= 100000000) or 
        (avg_length > 100 and avg_length <= 1000 and avg_cost_in_credits > 1000000 and avg_cost_in_credits <= 100000000) then 'medium starships'
        when (avg_crew > 100 and avg_cost_in_credits > 100000000) or 
        (avg_length > 1000 and avg_cost_in_credits > 100000000) then 'large starships'
    end as starship_group, --size classification
    case
        when avg_max_atmosphering_speed >= (2000 * 0.75) then 'high speed'
        when (avg_max_atmosphering_speed >= (2000 * 0.5)) and (avg_max_atmosphering_speed < (2000 * 0.75)) then 'medium speed'
        when (avg_max_atmosphering_speed < (2000 * 0.5)) then 'low speed'
    end as speed_classification --speed classification
from cte_view)

select * 
from cte_grouped
order by starship_group DESC NULLS LAST,  speed_classification DESC NULLS LAST
