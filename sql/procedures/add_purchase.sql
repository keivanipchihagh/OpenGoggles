CREATE OR REPLACE PROCEDURE purchase(
	user_id int,
	movie_id int
)
LANGUAGE plpgsql AS
$$ 
BEGIN
	-- Add purchase
	INSERT INTO purchases (movie_id, user_id, purchase_date) 
	VALUES ( movie_id, user_id, now());
	
	-- Reduce credits from user
	UPDATE users 
	SET
		credit = credit - (SELECT price FROM movies WHERE (movie_id = movies.id))
	WHERE
		users.id = user_id;
COMMIT;
END;
$$