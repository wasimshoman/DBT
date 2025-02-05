---
title: Manufacturer sellings.
---
> This page provides insights on the manufacturers of the Star Wars ships.


```distinct_Manufacturer
  select
      manufacturer,contributed_in_selling,helped_in_building
  from distinct_man
  limit 10
```
```averageBuildinggAmount
select avg(helped_in_building) as avg from postgres.distinct_man
```
```distinct_Manufacturer_no_limit
  select
      manufacturer,contributed_in_selling,helped_in_building
  from distinct_man
  order by contributed_in_selling desc

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



```KPIs
```
```total_manu
select count(*) as total_manu from postgres.distinct_man
```

Total number of distinct manufactureres : **<Value  data={total_manu} value=total_manu/>**.

<BarChart
  title = 'Top 10 Manufacturers Contributing to Building Starships' 
  data={distinct_Manufacturer}
  x=manufacturer
  y=helped_in_building
  xAxisTitle="Manufacturer"
	yAxisTitle="Built ships "
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

<DataTable data={distinct_Manufacturer_no_limit}/>