-- Select most popular genres among users (rented or purchased)
WITH u_m AS (
	-- Query total rented and purchased movies as (user_id, movie_id) unioned
	SELECT users.id AS user_id, purchases.movie_id
	FROM users
		INNER JOIN purchases ON purchases.user_id = users.id
		INNER JOIN movies ON movies.id = purchases.movie_id
	UNION ALL
	SELECT users.id AS user_id, rents.movie_id
	FROM users
		INNER JOIN rents ON rents.user_id = users.id
		INNER JOIN movies ON movies.id = rents.movie_id
),
m_g AS (
	-- Query all the movies and their corresponding genres (a movie can have multiple genres, therefor can be repeated multiple times)
	SELECT movies.id AS movie_id, genre
	FROM movies
		INNER JOIN movies_genres ON movies_genres.movie_id = movies.id
		INNER JOIN genres ON genres.id = movies_genres.genre_id
),
report AS (
	SELECT genre, COUNT(user_id) AS popularity
	FROM u_m
		INNER JOIN m_g USING(movie_id)
	GROUP BY genre
)
SELECT genre, popularity, DENSE_RANK() OVER (ORDER BY popularity DESC) AS rank
FROM (
	SELECT genre, COUNT(user_id) AS popularity
	FROM u_m
		INNER JOIN m_g USING(movie_id)
	GROUP BY genre
) AS report
ORDER BY popularity DESC