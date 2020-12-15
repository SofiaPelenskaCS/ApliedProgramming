from sqlalchemy import orm, VARCHAR, Date, BigInteger
#
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(1000))
    password = Column(VARCHAR(1000))
    passport = Column(VARCHAR(1000))
    adress = Column(VARCHAR(1000))
    money_amount = Column(Integer)
    telephone_number = Column(VARCHAR(1000))
    super_user = Column(Boolean)


class Banks(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True)
    per_cent = Column(Integer)
    all_money = Column(Integer)


class Credits(Base):
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


class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    sum = Column(BigInteger)
    credit_id = Column(Integer, ForeignKey(Credits.id))

    credit = orm.relationship(Credits, backref="transactions", lazy='joined')
