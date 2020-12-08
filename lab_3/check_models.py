from models import Session, Users, Banks, Credits, Transactions
import datetime
session = Session()

user = Users(id=3, email="lmao@o.o", passport="ok", password="1234", money_amount=12, telephone_number='1234567')
bank = Banks(id=3, per_cent=123, all_money=2323243)
credit = Credits(id=3, start_date=datetime.datetime.now().date(),
end_date=datetime.datetime.now().date(),
start_sum=1, current_sum=343, user=user, bank=bank)
transaction = Transactions(id=3, date=datetime.datetime.now().date(),
sum=1234, credit=credit)


session.add(user)
session.add(bank)
session.add(credit)
session.add(transaction)
session.commit()

print(session.query(Users).all())
print(session.query(Banks).all())
# print(session.query(Credits).all())
# print(session.query(Transactions).all())

session.close()