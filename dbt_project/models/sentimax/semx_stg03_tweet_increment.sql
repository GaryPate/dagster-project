
{{
    config(
        materialized='incremental'
    )
}}

select * from {{ source('SENTIMAX', 'tweet_data') }}