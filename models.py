
from sqlalchemy import orm
#
from app import db



class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(1000))
    password = db.Column(db.VARCHAR(1000))
    passport = db.Column(db.VARCHAR(1000))
    adress = db.Column(db.VARCHAR(1000))
    money_amount = db.Column(db.Integer)
    telephone_number = db.Column(db.VARCHAR(1000))



class Banks(db.Model):
    __tablename__ = "banks"

    id = db.Column(db.Integer, primary_key=True)
    per_cent = db.Column(db.Integer)
    all_money = db.Column(db.Integer)


class Credits(db.Model):
    __tablename__ = "credits"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_sum = db.Column(db.Integer)
    current_sum = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    bank_id = db.Column(db.Integer, db.ForeignKey(Banks.id))

    user = orm.relationship('Users', foreign_keys='Credits.user_id')
    bank = orm.relationship('Banks', foreign_keys='Credits.bank_id')


class Transactions(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    sum = db.Column(db.BigInteger)
    credit_id = db.Column(db.Integer, db.ForeignKey(Credits.id))

    credit = orm.relationship(Credits, backref="transactions", lazy='joined')