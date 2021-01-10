import json

import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Banks, Credits, Transactions
from requests.auth import HTTPBasicAuth
import hashlib
import datetime

engine = create_engine("postgresql://violetta:123456@localhost:5432/my_database")
Session = sessionmaker(bind=engine)
session = Session()


def test_post_add_user():
    url = "http://127.0.0.1:5000/add_user"

    payload = "{\n    \"email\" : \"bilyy@gmail.com\",\n    \"password\": \"123456\",\n    \"passport\": " \
              "\"EY74381\",\n    \"adress\": \"Kyiv\",\n    \"money_amount\": \"50000000\"," \
              "\n    \"telephone_number\": \"9138247282\",\n    \"super_user\": true\n} "
    headers = {
        'Authorization': 'Basic YmlseWJpbHk6MTIzNDU2Nzg5',
        'Content-Type': 'application/json'
    }

    resp = requests.request("POST", url, headers=headers, data=payload)

    assert resp.status_code == 200

    resp = requests.request("POST", url, headers=headers, data=payload)

    assert resp.status_code == 404

    session.query(Users).filter_by(email="bilyy@gmail.com").delete()
    session.commit()

    print(resp.text)


def test_show_user():
    url = "http://127.0.0.1:5000/show_user/1"

    user = Users(email="bilyvio@gmail.com",
                 password=hashlib.md5("123456".encode()).hexdigest(),
                 passport="HUI",
                 adress="Lviv",
                 money_amount=500000,
                 telephone_number="0930430540",
                 super_user=False)
    user.id = 1
    session.add(user)
    session.commit()

    resp = requests.get(url, auth=HTTPBasicAuth('bilyvio@gmail.com', '123456'))

    assert resp.status_code == 200

    assert resp.json()['passport'] == "HUI"

    session.query(Users).delete()
    session.commit()


def test_add_bank():
    url = "http://127.0.0.1:5000/new_bank"

    payload = "{\n    \"per_cent\" : 20,\n    \"all_money\": 50000\n}"
    headers = {
        'Authorization': 'Basic YmlseWJpbHlAZ21haWwuY29tOjEyMzQ1Ng==',
        'Content-Type': 'application/json'
    }

    user = Users(email="bilyviolmao@gmail.com",
                 password=hashlib.md5("123456".encode()).hexdigest(),
                 passport="EV1938",
                 adress="Kyiv",
                 money_amount=500000,
                 telephone_number="1384028419",
                 super_user=False)
    user.id = 1
    session.add(user)
    session.commit()

    resp = requests.post(url, data=payload, headers=headers, auth=HTTPBasicAuth('bilyviolmao@gmail.com', '123456'))

    assert resp.status_code == 403

    session.query(Users).filter_by(id=1).delete()
    session.commit()

    user1 = Users(email="bilyviolmao@gmail.com",
                  password=hashlib.md5("123456".encode()).hexdigest(),
                  passport="EV1938",
                  adress="Kyiv",
                  money_amount=500000,
                  telephone_number="1384028419",
                  super_user=True)
    user1.id = 1
    session.add(user1)
    session.commit()

    resp = requests.post(url, data=payload, headers=headers, auth=HTTPBasicAuth('bilyviolmao@gmail.com', '123456'))

    assert resp.status_code == 200

    assert session.query(Banks).first() is not None

    session.query(Users).delete()
    session.query(Banks).delete()
    session.commit()


def test_show_bank():
    url = "http://127.0.0.1:5000/show_bank_info/1"

    user = Users(email="bilyvio@gmail.com",
                 password=hashlib.md5("123456".encode()).hexdigest(),
                 passport="HUI",
                 adress="Lviv",
                 money_amount=500000,
                 telephone_number="0930430540",
                 super_user=False)
    user.id = 1
    session.add(user)
    session.commit()

    bank = Banks(per_cent=20, all_money=5000)
    bank.id = 1
    session.add(bank)
    session.commit()

    resp = requests.get(url, auth=HTTPBasicAuth('bilyvio@gmail.com', '123456'))

    assert resp.status_code == 200

    assert resp.json()['per_cent'] == 20

    session.query(Users).delete()
    session.query(Banks).delete()
    session.commit()


def test_add_credit():
    url = "http://127.0.0.1:5000/user/1/1/add_credit"

    payload = "{\n    \"start_date\": \"03/01/2020\",\n    \"end_date\": \"03/01/2020\",\n    \"start_sum\": 50000, \n    \"current_sum\": 100000\n}"
    headers = {
        'Authorization': 'Basic YmlseWJpbHlAZ21haWwuY29tOjEyMzQ1Ng==',
        'Content-Type': 'application/json'
    }

    user = Users(email="bilyvio@gmail.com",
                 password=hashlib.md5("123456".encode()).hexdigest(),
                 passport="HUI",
                 adress="Lviv",
                 money_amount=500000,
                 telephone_number="0930430540",
                 super_user=False)
    user.id = 1
    session.add(user)
    session.commit()

    bank = Banks(per_cent=20, all_money=5000)
    bank.id = 1
    session.add(bank)
    session.commit()

    credit = Credits(
        start_date=datetime.datetime(2020, 0o1, 0o3),
        end_date=datetime.datetime(2020, 0o1, 0o3),
        start_sum=50000,
        current_sum=100000,
        user_id=user.id,
        bank_id=bank.id)
    credit.id = 1
    session.add(credit)
    session.commit()

    resp = requests.post(url, data=payload, headers=headers, auth=HTTPBasicAuth('bilyvio@gmail.com', '123456'))

    assert resp.status_code == 200

    assert resp.json()['start_sum'] == 50000

    session.query(Credits).delete()
    session.query(Banks).delete()
    session.query(Users).delete()

    session.commit()


def test_show_сredit():
    url = "http://127.0.0.1:5000/user/1/show_credit"

    user = Users(email="bilyvio@gmail.com",
                 password=hashlib.md5("123456".encode()).hexdigest(),
                 passport="HUI",
                 adress="Lviv",
                 money_amount=500000,
                 telephone_number="0930430540",
                 super_user=False)
    user.id = 1
    session.add(user)
    session.commit()

    bank = Banks(per_cent=20, all_money=5000)
    bank.id = 1
    session.add(bank)
    session.commit()

    credit = Credits(
        start_date=datetime.datetime(2020, 0o1, 0o3),
        end_date=datetime.datetime(2020, 0o1, 0o3),
        start_sum=50000,
        current_sum=100000,
        user_id=user.id,
        bank_id=bank.id)
    credit.id = 1
    session.add(credit)
    session.commit()

    resp = requests.get(url, auth=HTTPBasicAuth('bilyvio@gmail.com', '123456'))

    assert resp.status_code == 200
    assert resp.json()[0]["current_sum"] == 100000

    session.query(Credits).delete()
    session.query(Banks).delete()
    session.query(Users).delete()


def test_add_transaction():
    url = "http://127.0.0.1:5000/user/1/1/add_transaction"

    payload = "\r\n{\r\n    \"date\" :\"03/01/2020\",\r\n    \"sum\" :50000\r\n}"
    headers = {
        'Authorization': 'Basic YmlseWJpbHlAZ21haWwuY29tOjEyMzQ1Ng==',
        'Content-Type': 'application/json'
    }

    user = Users(email="bilyvio@gmail.com",
                 password=hashlib.md5("123456".encode()).hexdigest(),
                 passport="HUI",
                 adress="Lviv",
                 money_amount=500000,
                 telephone_number="0930430540",
                 super_user=False)
    user.id = 1
    session.add(user)
    session.commit()

    bank = Banks(per_cent=20, all_money=5000)
    bank.id = 1
    session.add(bank)
    session.commit()

    credit = Credits(
        start_date=datetime.datetime(2020, 0o1, 0o3),
        end_date=datetime.datetime(2020, 0o1, 0o3),
        start_sum=50000,
        current_sum=100000,
        user_id=user.id,
        bank_id=bank.id)
    credit.id = 1
    session.add(credit)
    session.commit()

    resp = requests.post(url, data=payload, headers=headers, auth=HTTPBasicAuth('bilyvio@gmail.com', '123456'))

    assert resp.status_code == 200

    assert session.query(Transactions).first().sum == 50000

    session.query(Transactions).delete()
    session.query(Credits).delete()
    session.query(Banks).delete()
    session.query(Users).delete()

    session.commit()


def test_show_transaction():
    url = "http://127.0.0.1:5000/user/1/show_transaction"

    user = Users(email="bilyvio@gmail.com",
                 password=hashlib.md5("123456".encode()).hexdigest(),
                 passport="HUI",
                 adress="Lviv",
                 money_amount=500000,
                 telephone_number="0930430540",
                 super_user=False)
    user.id = 1
    session.add(user)
    session.commit()

    bank = Banks(per_cent=20, all_money=5000)
    bank.id = 1
    session.add(bank)
    session.commit()

    credit = Credits(
        start_date=datetime.datetime(2020, 0o1, 0o3),
        end_date=datetime.datetime(2020, 0o1, 0o3),
        start_sum=50000,
        current_sum=100000,
        user_id=user.id,
        bank_id=bank.id)
    credit.id = 1
    session.add(credit)
    session.commit()

    trans = Transactions(
        id=1,
        date=datetime.datetime(2020, 0o1, 0o3),
        sum=1212,
        credit_id=1)
    session.add(trans)
    session.commit()
    resp = requests.get(url, auth=HTTPBasicAuth('bilyvio@gmail.com', '123456'))

    assert resp.status_code == 200
    assert resp.json()[0]["sum"] == 1212

    session.query(Transactions).delete()
    session.query(Credits).delete()
    session.query(Banks).delete()
    session.query(Users).delete()
    session.commit()


if __name__ == '__main__':
    pytest.main()