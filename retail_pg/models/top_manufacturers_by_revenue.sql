WITH manufacturer_revenue_cte AS (
    SELECT
        manufacturer1 AS manufacturer,
        SUM(cost_in_credits) AS total_revenue
    FROM
        {{ ref('OBT_starships') }}
    GROUP BY
        manufacturer1

    UNION ALL

    SELECT
        manufacturer2 AS manufacturer,
        SUM(cost_in_credits) AS total_revenue
    FROM
        {{ ref('OBT_starships') }}
    WHERE
        manufacturer2 IS NOT NULL
    GROUP BY
        manufacturer2
)

SELECT
    manufacturer,
    SUM(total_revenue) AS total_revenue
FROM     manufacturer_revenue_cte
GROUP BY    manufacturer
ORDER BY total_revenue DESC NULLS LAST