# Revenue Breakdown

## Revenue by Starship Class and Manufacturer

This chart shows the top 10 starship classes and manufacturers by total revenue generated (based on `cost_in_credits`).

```revenue_breakdown
select * from postgres.revenue_breakdown
```

<BarChart 
  title="Top revenue by class and manufacturer" 
  data={revenue_breakdown}
  x="starship_class" 
  y="total_revenue" 
  series="manufacturer" 
  xAxisTitle="Starship class"
	yAxisTitle="Revenue"
/>