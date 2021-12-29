INSERT INTO people (id, first_name, last_name, is_married, email, nationality, birth_date)
VALUES
	( 1006, 'Keivan', 'Ipchi', 0, 'keivan@gmail.com', 'Iranian', '2001-02-09'),
	(1007, 'Reyhaneh', 'Jarchizadeh', 0, 'reyhaneh@gmail.com', 'Iranian', '1998-12-28');

INSERT INTO users (id, username, password, credit)
VALUES
	( 1006, 'Keivanipchi', '11111', 500),
	(1007, 'reyrey998', '22222', 500);

CREATE ROLE moviesdb
LOGIN
PASSWORD '12345';

GRANT ALL
ON ALL TABLES
IN SCHEMA public
TO moviesdb;

REVOKE all
ON TABLE genres
FROM moviesdb;

-- REASSIGN OWNED BY moviesdb TO postgres;  -- or some other trusted role
-- DROP OWNED BY moviesdb;
-- DROP ROLE moviesdb;