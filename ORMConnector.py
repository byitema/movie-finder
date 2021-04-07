import sqlalchemy
from sqlalchemy import Column, Table, MetaData, ForeignKey, PrimaryKeyConstraint, cast, text
from sqlalchemy import Integer, String, DateTime, SmallInteger, func, Float
from sqlalchemy.engine import Engine
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, sessionmaker, Session, Query
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from init import Base
import sqlite3
from Movie import Movie
import re
import configparser
from sqlalchemy.dialects import mysql


class ORMConnector(object):
    engine: AsyncEngine = None
    async_session = None
    metadata: MetaData = None
    PAGE_SIZE: int = None

    async def get_movies_list(self, page: int = 1, N: int = None, genres: str = None, year_from: int = None,
                              year_to: int = None,
                              regexp: str = None):
        async with self.async_session() as session:
            from_request = select(Movie, func.row_number().over(Movie.genre).label("row_num"))
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

            main_request = select(genre, movie_id, movie_name, year, rating, count_of_ratings)
            row_num = from_request.c.row_num
            if N is not None:
                main_request = main_request.where(row_num <= N)
            main_request_result = await session.execute(main_request)
            return main_request_result.paginate(page, self.PAGE_SIZE, False).items

    async def insert_new_rating(self, movie_id: int, rating: float):
        async with self.async_session() as session:
            movies_query = select(Movie).where(Movie.movie_id == movie_id)
            result = await session.execute(movies_query)
            for movie in result.all():
                temp_rating = movie.count_of_ratings * movie.rating
                temp_rating += rating
                movie.count_of_ratings += 1
                movie.rating = temp_rating
            await session.commit()


async def create_connector() -> ORMConnector:
    config = configparser.ConfigParser()
    config.read("configs/configs.ini")
    connector = ORMConnector()
    connector.PAGE_SIZE = config["MySQL"]["PAGE_SIZE"]
    connector.engine = create_async_engine(
        f"mysql+aiomysql://root:757020Key@localhost/tp_project_movies_db",
        echo=False)
    async with connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    connector.async_session = sessionmaker(bind=connector.engine, expire_on_commit=False, class_=AsyncSession)
    return connector
