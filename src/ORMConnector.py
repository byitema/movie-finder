import sqlalchemy
from sqlalchemy import Column, Table, MetaData, ForeignKey, PrimaryKeyConstraint
from sqlalchemy import Integer, String, DateTime, SmallInteger, func, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from init import Base
import sqlite3
from Movie import Movie
import re


class ORMConnector:
    engine: sqlalchemy.engine.Engine = None
    session: sqlalchemy.orm.Session = None
    metadata = None

    def __init__(self):
        self.engine = sqlalchemy.create_engine("mysql+pymysql://root:757020Key@localhost@port=3306/tp_project_movies_db",
                                               echo=None)
        # self.Base = declarative_base()
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.metadata.create_all(bind=self.engine)

    def get_movies_list(self, N: int = None, genres: str = None, year_from: int = None, year_to: int = None,
                        regexp: str = None):
        from_request = self.session.query(Movie, func.row_number().over(Movie.genre).label("row_num"))
        if genres is not None:
            from_request = from_request.where(Movie.genre in genres)
        if year_from is not None:
            from_request = from_request.where(year_from <= Movie.movie_year)
        if year_to is not None:
            from_request = from_request.where(year_to >= Movie.movie_year)
        if regexp is not None:
            from_request = from_request.where(re.match(regexp, Movie.movie_name))
        from_request = from_request.order_by(Movie.genre,Movie.rating.desc()).cte("temp")
        genre, movie_id, movie_name, year, rating, count_of_ratings,_ = from_request.c

        main_request = self.session.query(genre, movie_id, movie_name, year, rating, count_of_ratings)
        row_num = from_request.c.row_num
        if N is not None:
            main_request = main_request.where(row_num <= N)
        # print(main_request)
        return list(main_request.all())

    def insert_new_rating(self, movie_id: int, rating: float):
        # print(self.session.query(Movie).where(Movie.movie_id == movie_id))
        movies = self.session.query(Movie).where(Movie.movie_id == movie_id).all()
        for movie in movies:
            temp_rating = movie.count_of_ratings * movie.rating
            temp_rating += rating
            movie.count_of_ratings += 1
            movie.rating = temp_rating
        self.session.commit()


if __name__ == "__main__":
    orm = ORMConnector()
    # print(orm.session.execute("show tables from tp_project_movies_db;").fetchall())
    for movie in orm.get_movies_list(N=10, year_from=2010):
        print(movie)
    # orm.insert_new_rating(1, 4)
