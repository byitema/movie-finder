import sqlalchemy
from sqlalchemy import Column, Table, MetaData, ForeignKey, PrimaryKeyConstraint
from sqlalchemy import Integer, String, DateTime, SmallInteger, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

Base = declarative_base()