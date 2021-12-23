-- Query the box-office for each movie cross-tabed by date
SELECT *
FROM CROSSTAB('
	WITH m_c AS (
		SELECT movie_id, CONCAT(first_name, '' '', last_name) AS full_name
		FROM casts
			INNER JOIN people ON people.id = casts.people_id
	),
	m_g AS (
		SELECT movies.id AS movie_id, genre
		FROM movies
			INNER JOIN movies_genres ON movies_genres.movie_id = movies.id
			INNER JOIN genres ON genres.id = movies_genres.genre_id
	)
	SELECT full_name, genre, COUNT(genre)
	FROM m_c
		INNER JOIN m_g USING(movie_id)
	GROUP BY full_name, genre
	',
	'SELECT genre FROM genres'
) AS report(
	"full_name" VARCHAR,
	"Animation" VARCHAR,
	"Shi-Fi" VARCHAR,
	"Mystry" VARCHAR,
	"Sport" VARCHAR,
	"Family" VARCHAR,
	"Film-Noir" VARCHAR,
	"Game-Show" VARCHAR,
	"Westerb" VARCHAR,
	"Romance" VARCHAR,
	"Music" VARCHAR,
	"War" VARCHAR,
	"Horror" VARCHAR,
	"Action" VARCHAR,
	"Fantacy" VARCHAR,
	"Biography" VARCHAR,
	"Adventure" VARCHAR,
	"Comedy" VARCHAR,
	"Musical" VARCHAR,
	"Thriller" VARCHAR,
	"Crime" VARCHAR,
	"Drama" VARCHAR,
	"History" VARCHAR
)