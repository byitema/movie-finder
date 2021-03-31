DROP FUNCTION IF EXISTS FN_GET_NAME_FROM_TITLE;
# DELIMITER //
CREATE FUNCTION `FN_GET_NAME_FROM_TITLE`(
	title VARCHAR(256)
) RETURNS VARCHAR(256) CHARSET utf8mb4
    DETERMINISTIC
BEGIN
	DECLARE year_index TINYINT UNSIGNED;
    SET year_index = REGEXP_INSTR(title,"\\((([0-9]{4}\\-[0-9]{4})|([0-9]{4}))\\)\\s?$");
    IF year_index = 0 THEN
		RETURN TRIM(title);
	ELSE
		RETURN TRIM(SUBSTR(title,1,year_index-1));
	END IF;
END;
# DELIMITER //