from marshmallow import Schema, validate, fields
from marshmallow.validate import Range


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(validate=validate.Email())
    password = fields.String(validate=[validate.Length(max=50)])
    passport = fields.String(validate=[validate.Length(max=300)])
    adress = fields.String(validate=[validate.Length(max=100)])
    money_amount = fields.Integer()
    telephone_number = fields.String()


class CreditSchema(Schema):
    id = fields.Integer(dump_only=True)
    start_date = fields.Date()
    end_date = fields.Date()
    start_sum = fields.Integer()
    current_sum = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    bank_id = fields.Integer(dump_only=True)


class TransactionSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    sum = fields.Integer()
    credit_id = fields.Integer(dump_only=True)


class BankSchema(Schema):
    id = fields.Integer(dump_only=True)
    per_cent = fields.Integer()
    all_money = fields.Integer()