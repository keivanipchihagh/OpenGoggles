CREATE OR REPLACE FUNCTION checK_runtime()
RETURNS trigger
LANGUAGE 'plpgsql'
AS $$
BEGIN
IF (NEW.runtime < 200) THEN
RETURN NEW;
ELSE RAISE EXCEPTION 'runtime is over than normal size!';
END IF;
RETURN NULL;
END;
$$;

CREATE TRIGGER checK_runtime_trigger
BEFORE INSERT
ON movies
FOR EACH ROW 
EXECUTE PROCEDURE checK_runtime();
