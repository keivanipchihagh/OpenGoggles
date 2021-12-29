CREATE OR REPLACE FUNCTION permit_to_send()
RETURNS trigger
LANGUAGE 'plpgsql'
AS $$
BEGIN
IF (SELECT NEW.credit FROM users WHERE users.id = NEW.id) >=0  THEN

RETURN NEW;
ELSE RAISE EXCEPTION 'You dont have enough money to send to your friend :(';
END IF;
RETURN NULL;
END;
$$


CREATE TRIGGER send_permit
BEFORE UPDATE
ON users 
FOR EACH ROW 
EXECUTE PROCEDURE permit_to_send();