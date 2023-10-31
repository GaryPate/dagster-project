
{{
    config(
        materialized='incremental'
    )
}}

select * from {{ source('SENTIMAX', 'sentiment_staging') }}