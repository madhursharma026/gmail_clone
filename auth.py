from . import db
from .models import User
from datetime import date
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for


auth = Blueprint('auth', __name__)


first_name = ''
last_name = ''
email = ''
password = ''
confirm_password = ''
phone_no = ''
birth_month = ''
birth_date = ''
birth_year = ''
gender = ''

login_email = ''
login_password = ''


@auth.route("/login_email", methods=['GET', 'POST'])
def login_email_set():
    global login_email
    if request.method == 'POST':
        login_email = request.form.get('login_email')
        user_detail = User.query.filter_by(
            email=login_email, status='active').first()
        if user_detail:
            return redirect(url_for('auth.login_password_set'))
        else:
            flash("Email can't match", 'danger')
            return render_template("gmail_email_login.html")
    return render_template("gmail_email_login.html")


@auth.route("/login_password", methods=['GET', 'POST'])
def login_password_set():
    global login_email, login_password
    user_detail = User.query.filter_by(
        email=login_email, status='active').first()
    if request.method == 'POST':
        login_password = request.form.get('login_password')
        return redirect(url_for('auth.login'))
    return render_template("gmail_password_login.html", user_detail=user_detail)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    global login_email, login_password
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    email = login_email
    password = login_password
    user_detail = User.query.filter_by(email=email, status='active').first()
    if user_detail and check_password_hash(user_detail.password, password):
        login_user(user_detail, remember=True)
        db.session.commit()
        return redirect(url_for('views.home'))
    else:
        flash('Please Check Your Password', 'danger')
        return render_template("gmail_password_login.html", user_detail=user_detail)
    return render_template("gmail_password_login.html", user_detail=user_detail)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_email_set'))


@auth.route("/gmail_signup", methods=['GET', 'POST'])
def gmail_signup():
    global first_name, last_name, email, password, phone_no, birth_month, birth_date, birth_year, gender
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email_check = User.query.filter_by(email=email).first()
        if email_check:
            flash("Email already exists", "danger")
            return render_template("gmail_signup.html")
        if password == confirm_password:
            return redirect(url_for('auth.gmail_signup_next_page'))
        else:
            flash("password doesn't match with eatch other", "danger")
    return render_template("gmail_signup.html")


@auth.route("/gmail_signup_next_page", methods=['GET', 'POST'])
def gmail_signup_next_page():
    global first_name, last_name, email, password, phone_no, birth_month, birth_date, birth_year, gender
    if request.method == 'POST':
        phone_no = request.form.get('phone_no')
        birth_month = request.form.get('birth_month')
        birth_date = request.form.get('birth_date')
        birth_year = request.form.get('birth_year')
        gender = request.form.get('gender')
        today = date.today()
        user_age = today.year - \
            int(birth_year) - ((today.month, int(birth_date))
                               < (int(birth_month), int(birth_date)))
        if user_age >= 18:
            return redirect(url_for('auth.gmail_signup_next3_page'))
        else:
            flash(
                'Your age is not more than 18 yrs so, you are not allowed to make gmail', 'danger')
            return redirect(url_for('auth.gmail_signup_next_page'))
    return render_template("gmail_signup_next_page.html")


@auth.route("/gmail_signup_next3_page", methods=['GET', 'POST'])
def gmail_signup_next3_page():
    global first_name, last_name, email, password, phone_no, birth_month, birth_date, birth_year, gender
    if request.method == 'POST':
        new_user = User(firstname=first_name, lastname=last_name, email=email, password=generate_password_hash(
            password, method='sha256'), phone_no=phone_no, birth_month=birth_month, birth_date=birth_date, birth_year=birth_year, gender=gender)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!, Welcome to Gmail', 'success')
        user_detail = User.query.filter_by(
            email=email, status='active').first()
        if user_detail and check_password_hash(user_detail.password, password):
            login_user(user_detail, remember=True)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template("gmail_sign_up_next3_page.html")
