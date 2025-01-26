---
title: Starship model/class details
---
This dashboard provides insights into starship models, including their classification, selling performance, and technical specifications. Use the charts below to explore trends and patterns.


```starship_groups_agg
select * from postgres.starship_group_analysis
where starship_group <> '-'
```

```class_details
select * from postgres.class_details
limit 10
```
```averageSellingAmount
select avg(selling_count) as avg from postgres.class_details
```

```averageSpeed
select avg(avg_atmosphering_speed) as avg from postgres.class_details
```

```classifications
select * from postgres.classifications

```
```total_sales
select sum(selling_count) as total_sales from postgres.class_details
```

``` KPIs
```
```total_models
select count(distinct starship_class) as total_models from postgres.class_details
```





Total sold ships : <Value  data={total_sales} value=total_sales title="Total Units Sold" />.

Total distinct models :<Value  data={total_models} value=total_models title="Total Starship Models" />.


<BarChart
  title = 'Top 10 model selling amount for starship models' 
  data={class_details}
  x=starship_class
  y=selling_count
  xAxisTitle="Starship class"
	yAxisTitle="Number of units sold"
  xLabelWrap=true
>
  <ReferenceLine data={averageSellingAmount} y= avg label='average selling amount'/>
  
</BarChart>

<DataTable data={classifications}/>

## Grouping of starship models 

<BarChart 
    data={starship_groups_agg}
    title = 'Starship model group selling count' 
    x=starship_group
    y=total_starships
    xAxisTitle="Starship model group"
    yAxisTitle="Amount sold"
    seriesOrder={['small starships','medium starships','large starships']}
/>

## Details of starship groups
<BarChart 
    title = 'Average selling price for starship models' 
    data={classifications}
    x=starship_class
    y=avg_cost_in_credits
    series=starship_group
    seriesColors={{"large starships": "red", "medium starships": "blue","small starships": "black", 'null': 'gray'}}
    xAxisTitle="Starship class"
    yAxisTitle="Average selling price"
    xLabelWrap=true
    type=grouped
/>


<ScatterPlot 
  title = 'Average atmosphering speed for starship models' 
  data={classifications}
  x=starship_class
  y=avg_max_atmosphering_speed
  series=starship_group
  seriesColors={{"large starships": "red", "medium starships": "blue","small starships": "black", 'null': 'gray'}}
  xAxisTitle="Starship class"
  yAxisTitle="Average atmosphering speed"
  xLabelWrap=true
  type=grouped
>
  <ReferenceLine data={averageSpeed} y= avg label='average speed'/>
</ScatterPlot>

<ScatterPlot 
  title = 'Average length for starship models' 
  data={classifications}
  x=starship_class
  y=avg_length
  series=speed_classification
  seriesColors={{"high speed": "red", "medium speed": "blue","low speed": "black", 'null': 'gray'}}
  xAxisTitle="Starship class"
  yAxisTitle="Average ship length"
  xLabelWrap=true
  type=grouped
/>

