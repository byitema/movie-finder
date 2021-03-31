DROP PROCEDURE IF EXISTS sp_fill_movies;
# DELIMITER //
CREATE PROCEDURE `sp_fill_movies`()
BEGIN
	INSERT INTO movies(genre,movie_id,movie_name,movie_year,rating,count_of_ratings)
	WITH RECURSIVE cte_split_genres AS
	(
		SELECT stgm.movie_id, FN_GET_NAME_FROM_TITLE(stgm.title) AS `name`, FN_GET_YEAR_FROM_TITLE(stgm.title) AS `year`, FN_SPLIT_STR(stgm.genres_str,'|',1) AS genre,
		IF (
			LOCATE('|',stgm.genres_str)>0,
			SUBSTR(stgm.genres_str,LOCATE('|',stgm.genres_str)+1),
			''
		) AS other_genres_str
		FROM stg_movies as stgm
		UNION ALL
		SELECT movie_id, `name`, `year`, FN_SPLIT_STR(other_genres_str,'|',1),
		IF(
			LOCATE('|',other_genres_str)>0,
			SUBSTR(other_genres_str,LOCATE('|',other_genres_str)+1),
			''
		) AS other_genres_str
		FROM cte_split_genres
		WHERE other_genres_str <> ''
	),
	cte_group_ratings AS
	(
		SELECT movie_id,AVG(rating) AS rating,COUNT(*) as count_of_ratings
		FROM stg_ratings
		GROUP BY movie_id
	)
    SELECT sg.genre, sg.movie_id,sg.`name`,sg.`year`,smr.rating,smr.count_of_ratings
	FROM ( SELECT genre, movie_id, `name`, `year` FROM cte_split_genres ) AS sg
    LEFT JOIN ( SELECT movie_id,rating,count_of_ratings FROM cte_group_ratings ) AS smr
    ON sg.movie_id=smr.movie_id;
END;
# DELIMITER //