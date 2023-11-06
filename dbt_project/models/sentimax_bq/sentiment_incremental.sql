
{{
    config(
        materialized='incremental',
        tags=['sentimax-dbt']
    )
}}

select * from {{ source('SENTIMAX', 'st03_calc_sentiment') }}