WITH ranked_playlist AS (
  SELECT
    year_month,
    playlist_name,
    COUNT(*) AS row_count,
    RANK() OVER (PARTITION BY year_month ORDER BY COUNT(*) DESC) AS playlist_rank
  FROM "default"."spotify-tracker-sam-dynamodb-153v5770w5py5"
  WHERE year_month LIKE '2024%'
  GROUP BY year_month, playlist_name
)

SELECT playlist_name, year_month, row_count
FROM ranked_playlist
WHERE playlist_rank <= 10
ORDER BY year_month, row_count DESC
