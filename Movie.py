import sqlalchemy
from sqlalchemy import Column, Table, MetaData, ForeignKey, PrimaryKeyConstraint
from sqlalchemy import Integer, String, DateTime, SmallInteger, func, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from init import Base
import sqlite3


class Movie(Base):
    __tablename__ = "Movies"
    genre = Column(String(20), primary_key=True)
    movie_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    movie_name = Column(String(256), nullable=False)
    movie_year = Column(SmallInteger)
    rating = Column(Float)
    count_of_ratings = Column(Integer)

    def __init__(self, genre, movie_id, movie_name, movie_year, rating, count_of_ratings):
        self.rating = rating
        self.movie_year = movie_year
        self.movie_name = movie_name
        self.genre = genre
        self.movie_id = movie_id
        self.count_of_ratings = count_of_ratings

    def __repr__(self):
        return "%s, %s, %s, %s, %s, %s" % (
            self.genre, self.movie_id, self.movie_name, self.movie_year, self.rating, self.count_of_ratings)
