import mysql.connector
import csv
import glob
import configparser


def get_connection() -> mysql.connector.connection:
    """
    Connect to MySQl server

    :return: Connection-class object to MySQL database
    """
    config = configparser.ConfigParser()
    config.read("../configs/configs.ini")
    return mysql.connector.connect(host=config["MySQL"]["host"],
                                   user=config["MySQL"]["user"],
                                   password=config["MySQL"]["password"],
                                   database=config["MySQL"]["database"])


def execute_script(mysql_connection: mysql.connector.connection, sql_file_name: str) -> None:
    """
    Execute script from sql-file

    :param mysql_connection: Connection-class object to MySQL database
    :param sql_file_name: Name of sql-file
    :return: None
    """
    with open(file=sql_file_name, encoding="UTF-8") as sql_file:
        cursor = mysql_connection.cursor()
        for _ in cursor.execute(sql_file.read(), multi=True):
            pass
        mysql_connection.commit()
        cursor.close()


def main():
    conn = None
    try:
        conn = get_connection()
        for file in glob.iglob("../sql/*/ddl/*/*.sql"):
            execute_script(conn, file)

        insert_data_from_file(conn, "../sql/movies_db/dml/template/insert_movies_data_template.sql",
                              "../data/movies.csv")
        insert_data_from_file(conn, "../sql/movies_db/dml/template/insert_ratings_data_template.sql",
                              "../data/ratings.csv")

        execute_procedure(conn, "tp_project_movies_db.sp_fill_movies")
    except Exception as e:
        print(e)
    finally:
        conn.close()


def insert_data_from_file(mysql_connection: mysql.connector.connection, sql_insert_template_filename: str,
                          data_filename: str) -> None:
    """
    Insert data from csv-file into table in MySQL database

    :param mysql_connection: Connection-class object to MySQL database
    :param sql_insert_template_filename: Name of sql-insert_template file
    :param data_filename: Name of csv-file from which data will be inserted in table
    :return: None
    """
    mysql_cur = mysql_connection.cursor()
    with open(file=data_filename, encoding="UTF-8") as data, \
            open(file=sql_insert_template_filename, encoding="UTF-8") as template_file:
        query_str = template_file.read()
        data.readline()
        csv_data = csv.reader(data)
        for row in csv_data:
            mysql_cur.execute(query_str, row)
    mysql_connection.commit()
    mysql_cur.close()


def execute_procedure(mysql_connection: mysql.connector.connection, proc_name: str) -> None:
    """
    Execute procedure

    :param mysql_connection: Connection-class object to MySQL database
    :param proc_name: Name of procedure
    :return: None
    """
    cur = mysql_connection.cursor()
    cur.callproc(proc_name)
    mysql_connection.commit()
    cur.close()


if __name__ == "__main__":
    main()
