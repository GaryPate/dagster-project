
{{
    config(
        materialized='incremental',
        tags=['sentimax-dbt']
    )
}}

select * from {{ source('SENTIMAX', 'st02_tweet_json_to_bq') }}