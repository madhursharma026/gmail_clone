from sqlalchemy.sql.expression import null
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, datetime


# User me Fileds bnane hai
# phone no m null=true rakhna hai
# first_name, last_name, email, password, phone_no, birth_month, birth_date, birth_year, gender, date_joined, status
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32767), nullable=False)
    lastname = db.Column(db.String(32767), nullable=False)
    email = db.Column(db.String(32767), unique=True, nullable=False)
    password = db.Column(db.String(32767), nullable=False)
    phone_no = db.Column(db.String(10), nullable=True)
    birth_month = db.Column(db.String(2), nullable=False)
    birth_date = db.Column(db.String(2), nullable=False)
    birth_year = db.Column(db.String(4), nullable=False)
    gender = db.Column(db.String(32767), nullable=False)
    register_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(32767), nullable=False, default='active')
    sent_to_user_id = db.relationship(
        'Email', backref='sent_to_user_id', lazy=True)


# Emails me fileds bnane hai
# subject me default rakhna hai (No Subject)
class Email(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sent_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender = db.Column(db.Integer, nullable=False)
    email_subject = db.Column(
        db.String(32767), nullable=True, default='(No Subject)')
    email_content = db.Column(db.String(32767), nullable=False)
    email_status = db.Column(db.String(32767), nullable=False)
    email_star = db.Column(db.String(3), nullable=False, default='no')
    email_important = db.Column(db.String(3), nullable=False, default='no')
    read_status = db.Column(db.String(3), nullable=False, default='no')
    email_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
