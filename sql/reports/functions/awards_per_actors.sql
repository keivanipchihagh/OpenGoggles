CREATE OR REPLACE FUNCTION awards_per_actors(threshold INTEGER)
RETURNS TABLE (full_name TEXT, awards_count BIGINT)
LANGUAGE plpgsql
AS $$
#variable_conflict use_column
BEGIN
RETURN QUERY
	SELECT CONCAT(first_name, ' ', last_name) AS full_name, COUNT(title) AS awards_count
	FROM awards
		INNER JOIN people ON awards.people_id = people.id
	GROUP BY (full_name)
	HAVING COUNT(title) > threshold
	ORDER BY awards_count DESC;
END; $$