CREATE OR REPLACE FUNCTION rents_between(_rented_date DATE, _returned_date DATE)
RETURNS TABLE (first_name VARCHAR, last_name VARCHAR, title VARCHAR, rented_date DATE, returned_date DATE)
LANGUAGE plpgsql
AS $$
#variable_conflict use_column
BEGIN
RETURN QUERY
	-- Query users that have rented movies in an interval date
	SELECT first_name, last_name, title, rented_date, returned_date
	FROM rents
		INNER JOIN people ON rents.user_id = people.id
		INNER JOIN movies ON rents.movie_id = movies.id
	WHERE
		rented_date > _rented_date AND returned_date < _returned_date
	ORDER BY rented_date, returned_date;
END; $$