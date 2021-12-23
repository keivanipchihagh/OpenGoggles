WITH m_c AS (
	SELECT movie_id, CONCAT(first_name, ' ', last_name) AS full_name
	FROM casts
		INNER JOIN people ON people.id = casts.people_id
),
m_g AS (
	SELECT movies.id AS movie_id, genre
	FROM movies
		INNER JOIN movies_genres ON movies_genres.movie_id = movies.id
		INNER JOIN genres ON genres.id = movies_genres.genre_id
),
total AS (
	SELECT full_name, genre, COUNT(genre)
	FROM m_c
		INNER JOIN m_g USING(movie_id)
	GROUP BY full_name, genre
)
SELECT full_name, genre, SUM(count) AS count
FROM total
GROUP BY ROLLUP(full_name, genre)
ORDER BY full_name, genre