import sqlalchemy
from sqlalchemy import Column, Table, MetaData, ForeignKey, PrimaryKeyConstraint, cast, text
from sqlalchemy import Integer, String, DateTime, SmallInteger, func, Float
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from init import Base
import sqlite3
from Movie import Movie
import re
import configparser


class ORMConnector:
    engine: Engine = None
    session: Session = None
    metadata: MetaData = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("configs/configs.ini")
        self.engine = sqlalchemy.create_engine(
            f"mysql+pymysql://root:757020Key@localhost/tp_project_movies_db",
            echo=None)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.metadata.create_all(bind=self.engine)

    def get_movies_list(self, N: int = None, genres: str = None, year_from: int = None, year_to: int = None,
                        regexp: str = None):
        from_request = self.session.query(Movie, func.row_number().over(Movie.genre).label("row_num"))
        if genres is not None:
            from_request = from_request.where(func.locate(Movie.genre, genres) > 0)
        if year_from is not None:
            from_request = from_request.where(year_from <= Movie.movie_year)
        if year_to is not None:
            from_request = from_request.where(year_to >= Movie.movie_year)
        if regexp is not None:
            from_request = from_request.where(func.regexp_instr(Movie.movie_name, regexp) > 0)
        from_request = from_request.order_by(Movie.genre, Movie.rating.desc()).cte("temp")
        genre, movie_id, movie_name, year, rating, count_of_ratings, _ = from_request.c

        main_request = self.session.query(genre, movie_id, movie_name, year, rating, count_of_ratings)
        row_num = from_request.c.row_num
        if N is not None:
            main_request = main_request.where(row_num <= N)
        result_dict = {}
        for genre, movie_id, movie_name, movie_year, rating, count_of_ratings in main_request.all():
            if genre not in result_dict.keys():
                result_dict[genre] = []
            result_dict[genre].append(
                dict(movie_id=movie_id, movie_name=movie_name, movie_year=movie_year, rating=rating,
                     count_of_ratings=count_of_ratings))
        return result_dict

    def insert_new_rating(self, movie_id: int, rating: float):
        movies = self.session.query(Movie).where(Movie.movie_id == movie_id).all()
        for movie in movies:
            temp_rating = movie.count_of_ratings * movie.rating
            temp_rating += rating
            movie.count_of_ratings += 1
            movie.rating = temp_rating
        self.session.commit()
