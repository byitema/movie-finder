DROP TABLE IF EXISTS stg_ratings;
CREATE TABLE stg_ratings(
	user_id INT UNSIGNED NOT NULL,
    movie_id INT UNSIGNED NOT NULL,
    rating FLOAT,
    `timestamp` INT UNSIGNED,
    CONSTRAINT pk_stg_ratings PRIMARY KEY (user_id,movie_id)
);