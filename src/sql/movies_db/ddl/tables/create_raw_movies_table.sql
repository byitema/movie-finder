DROP TABLE IF EXISTS stg_movies;
CREATE TABLE stg_movies(
	movie_id INT UNSIGNED NOT NULL,
    title VARCHAR(256),
    genres_str VARCHAR(256),
    CONSTRAINT pk_stg_movies PRIMARY KEY(movie_id)
);