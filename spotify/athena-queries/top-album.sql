SELECT album, count (*) as row_count
FROM "default"."spotify-tracker-sam-dynamodb-153v5770w5py5"
WHERE year_month LIKE '2024%'
GROUP BY album
ORDER BY row_count DESC
LIMIT 10
