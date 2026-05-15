{{ config(materialized='table') }}

SELECT
    id,
    title,
    release_date,
    vote_average,
    vote_count,
    popularity
FROM {{ source('public', 'movies') }}
WHERE vote_average >= 7.5
AND vote_count >= 100
ORDER BY vote_average DESC