WITH ranked_songs AS (
  SELECT
    song,
    songID,
    artist,
    year_month,
    COUNT(*) AS play_count,
    RANK() OVER (PARTITION BY songID ORDER BY COUNT(*) DESC) AS song_rank
  FROM "default"."spotify-tracker-sam-dynamodb-153v5770w5py5"
  WHERE year_month LIKE '2024-09' AND cast(possibleduplicate as varchar) NOT LIKE 'true'
  GROUP BY songID, song, artist, year_month
)

SELECT song, artist, play_count, year_month
FROM ranked_songs
WHERE song_rank <= 100
ORDER BY year_month, play_count DESC
