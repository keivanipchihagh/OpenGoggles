CREATE TABLE "movies" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar(100),
  "type" varchar(20),
  "poster" varchar(200),
  "writer" varchar(50),
  "runtime" int,
  "released" date,
  "rated" varchar(10),
  "country" varchar(100),
  "language" varchar(100),
  "imdb_rating" float,
  "metacritic" int,
  "rotten_tomatoes" int,
  "box_office" int,
  "price" float,
  "plot" text
);

CREATE TABLE "movies_genres" (
  "movie_id" int,
  "genre_id" int,
  PRIMARY KEY ("movie_id", "genre_id")
);

CREATE TABLE "genres" (
  "id" SERIAL PRIMARY KEY,
  "genre" varchar(50)
);

CREATE TABLE "people" (
  "id" SERIAL PRIMARY KEY,
  "first_name" varchar(50),
  "last_name" varchar(50),
  "is_married" int,
  "email" varchar(50),
  "nationality" varchar(30),
  "birth_date" date
);

CREATE TABLE "casts" (
  "people_id" int,
  "movie_id" int,
  "role" varchar(50),
  "contract" text,
  PRIMARY KEY ("people_id", "movie_id")
);

CREATE TABLE "directors" (
  "people_id" int,
  "movie_id" int,
  "contract" text,
  PRIMARY KEY ("people_id", "movie_id")
);

CREATE TABLE "awards" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar(100),
  "people_id" int,
  "movie_id" int,
  "issued_date" date
);

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar(50),
  "password" varchar(50),
  "credit" int
);

CREATE TABLE "users_movies" (
  "user_id" int,
  "movie_id" int,
  PRIMARY KEY ("user_id", "movie_id")
);

CREATE TABLE "rents" (
  "movie_id" int,
  "user_id" int,
  "rented_date" date,
  "returned_date" date,
  PRIMARY KEY ("movie_id", "user_id")
);

CREATE TABLE "purchases" (
  "movie_id" int,
  "user_id" int,
  "purchase_date" date,
  PRIMARY KEY ("movie_id", "user_id")
);

ALTER TABLE "movies_genres" ADD FOREIGN KEY ("movie_id") REFERENCES "movies" ("id");

ALTER TABLE "movies_genres" ADD FOREIGN KEY ("genre_id") REFERENCES "genres" ("id");

ALTER TABLE "casts" ADD FOREIGN KEY ("people_id") REFERENCES "people" ("id");

ALTER TABLE "casts" ADD FOREIGN KEY ("movie_id") REFERENCES "movies" ("id");

ALTER TABLE "directors" ADD FOREIGN KEY ("people_id") REFERENCES "people" ("id");

ALTER TABLE "directors" ADD FOREIGN KEY ("movie_id") REFERENCES "movies" ("id");

ALTER TABLE "awards" ADD FOREIGN KEY ("people_id") REFERENCES "people" ("id");

ALTER TABLE "awards" ADD FOREIGN KEY ("movie_id") REFERENCES "movies" ("id");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "people" ("id");

ALTER TABLE "users_movies" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "users_movies" ADD FOREIGN KEY ("movie_id") REFERENCES "movies" ("id");

ALTER TABLE "rents" ADD FOREIGN KEY ("movie_id") REFERENCES "movies" ("id");

ALTER TABLE "rents" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "purchases" ADD FOREIGN KEY ("movie_id") REFERENCES "movies" ("id");

ALTER TABLE "purchases" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

