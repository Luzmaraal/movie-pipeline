{{ config(materialized='table') }}

SELECT
    id,
    title,
    release_date,
    popularity,
    vote_average,
    vote_count
FROM {{ source('public', 'movies') }}
ORDER BY popularity DESC
LIMIT 20