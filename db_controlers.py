from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Users, Banks, Credits, Transactions
from flask import request, jsonify, json, Flask
from schemas import UserSchema, CreditSchema, TransactionSchema, BankSchema
import hashlib
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

engine = create_engine("postgresql://violetta:123456@localhost:5432/my_database")
Session = sessionmaker(bind=engine)
session = Session()


@auth.get_user_roles
def get_user_roles(cur_user):
    user = session.query(Users).filter_by(email=cur_user.username).first()
    if user.super_user:
        return 'admin'
    return 'user'


@app.route('/new_bank', methods=['POST'])
@auth.login_required(role='admin')
def bank():
    per_cent = request.json.get('per_cent', None)
    all_money = request.json.get('all_money', None)
    new_bank = Banks(per_cent=per_cent, all_money=all_money)
    session.add(new_bank)
    session.commit()
    schemas = BankSchema()
    return jsonify(schemas.dump(new_bank)), 200


@app.route('/show_bank_info/<id>', methods=['GET'])
@auth.login_required
def show_bank_id(id):
    bank = session.query(Banks).filter_by(id=id).first()
    if bank is None:
        return jsonify({"msg": "Not Found"}), 404
    schemas = BankSchema()
    return jsonify(schemas.dump(bank)), 200


@app.route('/add_user', methods=['POST'])
def create_user():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    passport = request.json.get('passport', None)
    adress = request.json.get('adress', None)
    money_amount = request.json.get('money_amount', None)
    telephone_number = request.json.get('telephone_number', None)
    super_user = request.json.get('super_user', False)
    if session.query(Users).filter_by(email=email).first() is None:
        new_user = Users(email=email,
                         password=hashlib.md5(password.encode()).hexdigest(),
                         passport=passport,
                         adress=adress,
                         money_amount=money_amount,
                         telephone_number=telephone_number,
                         super_user=super_user)
        session.add(new_user)
        session.commit()
        schemas = UserSchema()
        return jsonify(schemas.dump(new_user)), 200
    return jsonify({"msg": "Email is already in use"}), 404


@app.route('/show_user/<id>', methods=['GET'])
@auth.login_required
def show_user(id):
    user = session.query(Users).filter_by(id=id).first()
    if user is not None:
        schemas = UserSchema()
        return jsonify(schemas.dump(user))
    return jsonify({"msg": "Not Found"}), 404


@auth.verify_password
def verify_password(email, password):
    return session.query(Users).filter_by(email=email,
                                 password=hashlib.md5(password.encode()).hexdigest()).first() is not None


@app.route('/user/<id>/<bankId>/add_credit', methods=['POST'])
@auth.login_required
def create_credit(id, bankId):
    user = session.query(Users).filter_by(id=id).first()
    bank = session.query(Banks).filter_by(id=bankId).first()
    if user is None:
        return jsonify({"msg": "Not Found"}), 404
    if bank is None:
        return jsonify({"msg": "Not Found"}), 404
    start_date = request.json.get('start_date', None)
    end_date = request.json.get('end_date', None)
    start_sum = request.json.get('start_sum', None)
    user_id = user.id
    bank_id = bank.id
    bank.all_money -= start_sum
    new_credit = Credits(
        start_date=start_date,
        end_date=end_date,
        start_sum=start_sum,
        current_sum=start_sum,
        user_id=user_id,
        bank_id=bank_id)
    session.add(new_credit)
    session.commit()
    schemas = CreditSchema()
    return jsonify(schemas.dump(new_credit)), 200


@app.route('/user/<id>/show_credit', methods=['GET'])
@auth.login_required
def show_credit(id):
    credits = session.query(Credits).filter_by(user_id=id).all()
    if credits is not None:
        schemas = CreditSchema(many=True)
        return jsonify(schemas.dump(credits)), 200
    return jsonify({"msg": "Not Found"}), 404


@app.route('/user/<bankId>/<creditId>/add_transaction', methods=['POST'])
@auth.login_required
def add_transaction(bankId, creditId):
    credit = session.query(Credits).filter_by(id=creditId).first()
    bank = session.query(Banks).filter_by(id=bankId).first()
    if credit is None:
        return jsonify({"msg": "Not Found"}), 404
    if bank is None:
        return jsonify({"msg": "Not Found"}), 404
    date = request.json.get('date', None)
    sum = request.json.get('sum', None)
    credit_id = credit.id
    new_transaction = Transactions(
        date=date,
        sum=sum,
        credit_id=credit_id)
    bank.all_money += sum
    credit.current_sum -= sum
    session.add(new_transaction)
    session.commit()
    schemas = TransactionSchema()
    return jsonify(schemas.dump(new_transaction)), 200


@app.route('/user/<creditId>/show_transaction', methods=['GET'])
@auth.login_required
def show_transaction(creditId):
    transactions = session.query(Transactions).filter_by(credit_id=creditId).all()
    if transactions is not None:
        schemas = TransactionSchema(many=True)
        return jsonify(schemas.dump(transactions)), 200
    return jsonify({"msg": "Not Found"}), 404


if __name__ == '__main__':
    app.run()
