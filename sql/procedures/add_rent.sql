CREATE OR REPLACE PROCEDURE rent(
	renter_id int,
	movie_id int
)
LANGUAGE plpgsql AS
$$ 
BEGIN
IF (SELECT credit FROM users WHERE users.id=renter_id) >= (SELECT price / 2 FROM movies WHERE movies.id = movie_id) THEN
	
	-- Add a new rent
	INSERT into rents (movie_id, user_id, rented_date) 
	VALUES ( movie_id, renter_id, now());
	
	-- Update credit (half price)
	UPDATE users 
	SET
		credit = credit - (SELECT price / 2 FROM movies WHERE (movie_id = movies.id))
	WHERE
		users.id = renter_id;
ELSE
RAISE EXCEPTION 'you dont have enough money for renting movie!';
END IF;
COMMIT;
END;
$$