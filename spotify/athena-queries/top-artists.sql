// Top Artists

WITH ranked_artists AS (
  SELECT
    artist,
    year_month,
    COUNT(*) AS play_count,
    RANK() OVER (PARTITION BY year_month ORDER BY COUNT(*) DESC) AS artist_rank
  FROM "default"."spotify-tracker-sam-dynamodb-153v5770w5py5"
  WHERE year_month LIKE '2024-%' AND cast(possibleduplicate as varchar) NOT LIKE 'true'
  GROUP BY year_month, artist
)

SELECT artist, year_month, play_count
FROM ranked_artists
WHERE artist_rank <= 10
ORDER BY year_month, play_count DESC
