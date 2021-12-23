CREATE OR REPLACE FUNCTION movies_by_actor(firstname VARCHAR, lastname VARCHAR)
RETURNS TABLE (title VARCHAR, writer VARCHAR, released DATE, plot TEXT)
LANGUAGE plpgsql
AS $$
#variable_conflict use_column
BEGIN
RETURN QUERY
	-- Query the movies a spesific actor/actress has played in
	WITH actors AS (
		-- Query all actors/actresses names as (first_name, last_name)
		SELECT movie_id, first_name, last_name
		FROM casts
			INNER JOIN people ON people.id = casts.people_id
	)
	SELECT title, writer, released, plot
	FROM actors
		INNER JOIN movies ON actors.movie_id = movies.id
	WHERE
		first_name = firstname AND last_name = lastname;
END; $$