import os

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    BigInteger,
    DateTime,
    func,
    Date
)
from sqlalchemy import orm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URI = os.getenv("DB_URI", "postgres://postgres:dagger@localhost:5432/postgres")
engine = create_engine(DB_URI)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

BaseModel = declarative_base()

class Users(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    passport = Column(String)
    adress = Column(String)
    money_amount = Column(Integer)
    telephone_number = Column(String)


class Banks(BaseModel):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True)
    per_cent = Column(Integer)
    all_money = Column(Integer)    


class Credits(BaseModel):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    start_sum = Column(Integer)
    current_sum = Column(Integer)
    user_id = Column(Integer, ForeignKey(Users.id))
    bank_id = Column(Integer, ForeignKey(Banks.id))

    user = orm.relationship('Users', foreign_keys='Credits.user_id')
    bank = orm.relationship('Banks', foreign_keys='Credits.bank_id')


class Transactions(BaseModel):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    sum = Column(BigInteger) 
    credit_id = Column(Integer, ForeignKey(Credits.id))

    credit = orm.relationship(Credits, backref="transactions", lazy='joined')