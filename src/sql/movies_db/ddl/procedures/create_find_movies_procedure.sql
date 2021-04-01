DROP PROCEDURE IF EXISTS sp_find_movies;
# DELIMITER //
CREATE PROCEDURE `sp_find_movies`(
	IN N INT UNSIGNED,
    IN genres VARCHAR(256),
    IN year_from SMALLINT,
    IN year_to SMALLINT,
    IN reg_exp VARCHAR(256)
)
BEGIN
    SELECT temp.genre,temp.movie_id,temp.movie_name,temp.movie_year,temp.rating
    FROM (
		SELECT *, ROW_NUMBER() OVER (PARTITION BY m.genre) AS rows_count
		FROM movies_db.movies as m
		WHERE 	(LOCATE(m.genre,genres) > 0 OR genres IS NULL) AND
				(year_from <= m.movie_year OR year_from IS NULL) AND
				(year_to >= m.movie_year OR year_to IS NULL) AND
				(REGEXP_INSTR(m.movie_name,reg_exp) > 0 OR reg_exp IS NULL)
		ORDER BY m.genre,m.rating DESC
    ) AS temp
    WHERE temp.rows_count<=N OR N IS NULL;
END;
# DELIMITER //