
---
title: Manufacturer sellings
---


```distinct_Manufacturer
  select
      *
  from distinct_man
  limit 10
```
```averageBuildinggAmount
select avg(helped_in_building) as avg from postgres.distinct_man
```


```manufacturer_sellings
  select
      *
  from manufacturer_sellings
  limit 10
```
```averageSellingAmount
select avg(selling_count) as avg from postgres.manufacturer_sellings
```


<BarChart
  title = 'Top 10 manufacturers contribute in building starships' 
  data={distinct_Manufacturer}
  x=manufacturer
  y=helped_in_building
  xAxisTitle="Manufacturer"
	yAxisTitle="# of built ships "
  xLabelWrap=true
>
  <ReferenceLine data={averageBuildinggAmount} y= avg label='average built amount'/>
</BarChart>

<ScatterPlot 
  data={distinct_Manufacturer}
  title = 'Amout of contributed selling credits for each manufacturers' 
  x=manufacturer
  y=contributed_in_selling
  xAxisTitle="Manufacturer"
  yAxisTitle="Amount in credits"
  yMin= 0
  sort=true
  shape= diamond
  xLabelWrap=true
/>

