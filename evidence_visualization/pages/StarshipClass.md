---
title: Starship class details
---


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

<BarChart
  title = 'Top 10 mosel selling amount for starship models' 
  data={class_details}
  x=starship_class
  y=selling_count
  xAxisTitle="Starship class"
	yAxisTitle="Selling count"
  xLabelWrap=true
>
  <ReferenceLine data={averageSellingAmount} y= avg label='average selling amount'/>
</BarChart>

<DataTable data={classifications}/>


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
