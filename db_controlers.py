from models import Users, Banks, Credits, Transactions
from app import app
from app import db
from flask import request, jsonify, json
from schemas import UserSchema, CreditSchema,TransactionSchema,BankSchema
import hashlib


@app.route('/new_bank', methods=['POST'])
def bank():
    per_cent = request.json.get('per_cent', None)
    all_money = request.json.get('all_money', None)
    new_bank = Banks(per_cent=per_cent, all_money=all_money)
    db.session.add(new_bank)
    db.session.commit()
    schemas = BankSchema()
    return jsonify(schemas.dump(new_bank)), 200


@app.route('/show_bank_info/<id>', methods=['GET'])
def show_bank_id(id):
    bank = Banks.query.filter_by(id=id).first()
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
    if Users.query.filter_by(email=email).first() is None:
        new_user = Users(email=email,
                         password= hashlib.md5(password.encode()).hexdigest(),
                         passport=passport,
                         adress=adress,
                         money_amount=money_amount,
                         telephone_number=telephone_number)
        db.session.add(new_user)
        db.session.commit()
        schemas = UserSchema()
        return jsonify(schemas.dump(new_user)),200
    return jsonify({"msg": "Email is already in use"}), 404


@app.route('/show_user/<id>', methods=['GET'])
def show_user(id):
    user = Users.query.filter_by(id=id).first()
    if user is not None:
        schemas = UserSchema()
        return jsonify(schemas.dump(user))
    return jsonify({"msg": "Not Found"}), 404


@app.route('/user/<id>/<bankId>/add_credit', methods=['POST'])
def create_credit(id, bankId):
    user = Users.query.filter_by(id=id).first()
    bank = Banks.query.filter_by(id=bankId).first()
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
    db.session.add(new_credit)
    db.session.commit()
    schemas = CreditSchema()
    return jsonify(schemas.dump(new_credit)), 200


@app.route('/user/<id>/show_credit', methods=['GET'])
def show_credit(id):
    credits = Credits.query.filter_by(user_id=id).all()
    if credits is not None:
        schemas = CreditSchema(many=True)
        return jsonify(schemas.dump(credits)), 200
    return jsonify({"msg": "Not Found"}), 404


@app.route('/user/<bankId>/<creditId>/add_transaction', methods=['POST'])
def add_transaction(bankId, creditId):
    credit = Credits.query.filter_by(id=creditId).first()
    bank = Banks.query.filter_by(id=bankId).first()
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
    db.session.add(new_transaction)
    db.session.commit()
    schemas = TransactionSchema()
    return jsonify(schemas.dump(new_transaction)), 200


@app.route('/user/<creditId>/show_transaction', methods=['GET'])
def show_transaction(creditId):
    transactions = Transactions.query.filter_by(credit_id=creditId).all()
    if transactions is not None:
        schemas = TransactionSchema(many=True)
        return jsonify(schemas.dump(transactions)), 200
    return jsonify({"msg": "Not Found"}), 404
