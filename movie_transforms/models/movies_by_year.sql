{{ config(materialized='table') }}

SELECT
    EXTRACT(YEAR FROM release_date::date) AS release_year,
    COUNT(*) AS total_movies,
    ROUND(AVG(vote_average)::numeric, 2) AS avg_rating,
    ROUND(AVG(popularity)::numeric, 2) AS avg_popularity
FROM {{ source('public', 'movies') }}
WHERE release_date IS NOT NULL
AND release_date != ''
GROUP BY release_year
ORDER BY release_year DESC