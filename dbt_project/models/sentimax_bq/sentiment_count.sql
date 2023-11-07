
{{
    config(
        tags=['sentimax-dbt']
    )
}}

WITH getval AS (
    SELECT 
    load_datetime as time, 
    sentiment, 
    COUNT(id) as Value,
    FROM {{ ref('sentiment_incremental') }}
    GROUP BY load_datetime, sentiment
),
pivotcounts AS (
    SELECT * FROM
    getval
    PIVOT(SUM(Value) FOR sentiment IN ('positive', 'neutral', 'negative'))
)
SELECT * FROM pivotcounts;
