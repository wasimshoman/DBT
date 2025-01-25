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
<BarChart
  title = 'Seeling amount for starship models' 
  data={class_details}
  x=starship_class
  y=selling_count
  xAxisTitle="Starship class"
	yAxisTitle="Selling amount"
  xLabelWrap=true
  color="#1f77b4" 
>
  <ReferenceLine data={averageSellingAmount} y= avg label='average selling amount'/>
</BarChart>

<BarChart
  title = 'Average seeling price for starship models' 
  data={class_details}
  x=starship_class
  y=avg_selling_price
  xAxisTitle="Starship class"
	yAxisTitle="Average selling price"
  xLabelWrap=true
  color="#ff7f0e"
/>

<ScatterPlot 
  title = 'Average atmosphering speed for starship models' 
  data={class_details}
  x=starship_class
  y=avg_atmosphering_speed
  xAxisTitle="Starship class"
	yAxisTitle="Average atmosphering speed"
  swapXY=true
  xLabelWrap=true
  color="#2ca02c" 
>
  <ReferenceLine data={averageSpeed} y= avg label='average speed'/>
</ScatterPlot>

