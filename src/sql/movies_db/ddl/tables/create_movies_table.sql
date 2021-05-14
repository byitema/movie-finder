DROP TABLE IF EXISTS movies;
CREATE TABLE movies(
	genre VARCHAR(20),
    movie_id INT UNSIGNED,
    movie_name VARCHAR(256) NOT NULL,
    movie_year SMALLINT,
    rating FLOAT,
    count_of_ratings INTEGER,
    CONSTRAINT pk_movies PRIMARY KEY(genre,movie_id)
);