CREATE OR REPLACE PROCEDURE gift(
	purcher_id int,
	friend_id int,
	movie_id int
)
LANGUAGE plpgsql AS
$$ 

BEGIN
	-- Decrease price from the user that is buying the gift
	UPDATE users
	SET
		credit = credit - (SELECT price FROM movies WHERE (movie_id = movies.id))
	WHERE
		users.id = purcher_id;
 
	INSERT INTO purchases (movie_id, user_id, purchase_date) 
	VALUES
		( movie_id, friend_id, now());
COMMIT;
END;
$$