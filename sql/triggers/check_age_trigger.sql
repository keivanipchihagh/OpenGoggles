CREATE OR REPLACE FUNCTION check_age()
RETURNS TRIGGER
LANGUAGE 'plpgsql'
AS $$
BEGIN
-- One must be more than 17 years old
IF (SELECT date_part('year', now()) - date_part('year', birth_date) FROM people WHERE id = NEW.user_id ) > 17 THEN
	RETURN NEW;
-- Otherwise, raise error
ELSE RAISE EXCEPTION 'Dude, you are too young for this!';
END IF;
RETURN NULL;	-- Doesn't do anything, but jic
END;
$$;

CREATE TRIGGER check_age_trigger
BEFORE INSERT
ON purchases 
FOR EACH ROW 
EXECUTE PROCEDURE check_age();