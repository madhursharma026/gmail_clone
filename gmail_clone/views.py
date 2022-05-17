from re import U
from sqlalchemy.sql.expression import insert
from . import db
from sqlalchemy import func
from flask_login import login_required, current_user
from .models import User, Email
from datetime import date, datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify


views = Blueprint('views', __name__)


@views.route("/")
@login_required
def home():
    temporary_sender_list = []
    sender_list = []
    getting_emails = Email.query.filter(
        Email.sent_to == current_user.id, Email.email_status == 'inbox').order_by(Email.email_time.desc()).all()
    for getting_emails_sender in getting_emails:
        temporary_sender_list.append(getting_emails_sender.sender)
    for temporary_sender_list in temporary_sender_list:
        sender_user_detail = User.query.filter(
            User.id == temporary_sender_list).all()
        for sender_user_detail in sender_user_detail:
            sender_list.append(sender_user_detail.email)
    return render_template("gmail_inbox.html", getting_emails=getting_emails, sender_list=sender_list)


@views.route("/single_email/email_id:<id>", methods=['GET', 'POST'])
@login_required
def single_email(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    getting_detail_of_sender = User.query.filter(
        User.id == getting_email_detail.sender).first()
    getting_email_detail.read_status = 'yes'
    db.session.commit()
    return render_template("gmail_single_email.html", getting_email_detail=getting_email_detail, getting_detail_of_sender=getting_detail_of_sender)


@views.route("/bin_single_email/email_id:<id>", methods=['GET', 'POST'])
@login_required
def bin_single_email(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    getting_detail_of_sender = User.query.filter(
        User.id == getting_email_detail.sender).first()
    getting_email_detail.read_status = 'yes'
    db.session.commit()
    return render_template("gmail_bin_single_email.html", getting_email_detail=getting_email_detail, getting_detail_of_sender=getting_detail_of_sender)


@views.route("/delete_email_inbox/email_id:<id>", methods=['GET', 'POST'])
@login_required
def delete_email_inbox(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    getting_email_detail.email_status = 'bin'
    db.session.commit()
    return redirect(url_for('views.home'))


@views.route("/delete_email_sent/email_id:<id>", methods=['GET', 'POST'])
@login_required
def delete_email_sent(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sender == current_user.id).first()
    getting_email_detail.email_status = 'bin'
    db.session.commit()
    return redirect(url_for('views.sent_email'))


@views.route("/star_email_sent/email_id:<id>", methods=['GET', 'POST'])
@login_required
def star_email_sent(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sender == current_user.id).first()
    if getting_email_detail.email_star == 'no':
        getting_email_detail.email_star = 'yes'
        db.session.commit()
    else:
        getting_email_detail.email_star = 'no'
        db.session.commit()
    return redirect(request.referrer)


@views.route("/important_email_sent/email_id:<id>", methods=['GET', 'POST'])
@login_required
def important_email_sent(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sender == current_user.id).first()
    if getting_email_detail.email_important == 'no':
        getting_email_detail.email_important = 'yes'
        db.session.commit()
    else:
        getting_email_detail.email_important = 'no'
        db.session.commit()
    return redirect(request.referrer)


@views.route("/star_email_inbox/email_id:<id>", methods=['GET', 'POST'])
@login_required
def star_email_inbox(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    if getting_email_detail.email_star == 'no':
        getting_email_detail.email_star = 'yes'
        db.session.commit()
    else:
        getting_email_detail.email_star = 'no'
        db.session.commit()
    return redirect(request.referrer)


@views.route("/important_email_inbox/email_id:<id>", methods=['GET', 'POST'])
@login_required
def important_email_inbox(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    if getting_email_detail.email_important == 'no':
        getting_email_detail.email_important = 'yes'
        db.session.commit()
    else:
        getting_email_detail.email_important = 'no'
        db.session.commit()
    return redirect(request.referrer)


@views.route("/delete_email_important/email_id:<id>", methods=['GET', 'POST'])
@login_required
def delete_email_important(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    getting_email_detail.email_status = 'bin'
    db.session.commit()
    return redirect(url_for('views.important_emails'))


@views.route("/delete_email_starred/email_id:<id>", methods=['GET', 'POST'])
@login_required
def delete_email_starred(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    getting_email_detail.email_status = 'bin'
    db.session.commit()
    return redirect(url_for('views.starred'))


@views.route("/permanent_delete/email_id:<id>", methods=['GET', 'POST'])
@login_required
def permanent_delete(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id, Email.email_status == 'bin').first()
    getting_email_detail.email_status = 'permanent delete'
    db.session.commit()
    return redirect(url_for('views.bin_email'))


@views.route("/restore_email/email_id:<id>", methods=['GET', 'POST'])
@login_required
def restore_delete(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    getting_email_detail.email_status = 'inbox'
    db.session.commit()
    return redirect(url_for('views.bin_email'))


@views.route("/sent_email")
@login_required
def sent_email():
    getting_mail_details = Email.query.filter(
        Email.email_status == 'inbox', Email.sender == current_user.id).order_by(Email.email_time.desc()).all()
    return render_template("gmail_sent_email.html", getting_mail_details=getting_mail_details)


@views.route("/sent_single_email/<id>")
@login_required
def sent_single_email(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sender == current_user.id).first()
    getting_email_detail.read_status = 'yes'
    db.session.commit()
    return render_template("gmail_sent_single_email.html", getting_email_detail=getting_email_detail)


@views.route("/compose_email_form", methods=['GET', 'POST'])
@login_required
def compose_email_form():
    if request.method == 'POST':
        email_send_to = request.form.get('email_send_to')
        email_subject = request.form.get('email_subject')
        email_content = request.form.get('email_content')
        send_to_detail = User.query.filter_by(
            email=email_send_to, status='active').first()
        if send_to_detail:
            new_email = Email(sent_to=send_to_detail.id, sender=current_user.id,
                              email_subject=email_subject, email_content=email_content, email_status='inbox')
            db.session.add(new_email)
            db.session.commit()
            flash('Email sent successfully', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('Email not found', 'danger')
            return redirect(url_for('views.compose_email_form'))
    return render_template("gmail_compose_email.html")


@views.route("/reply_email_form/email:id<id>", methods=['GET', 'POST'])
@login_required
def reply_email_form(id):
    getting_email_detail = Email.query.filter(Email.id == id).first()
    if request.method == 'POST':
        email_send_to_detail = User.query.filter(User.email == request.form.get(
            'email_sent_to'), User.status == 'active').first()
        email_send_to = email_send_to_detail.id
        email_subject = getting_email_detail.email_subject
        email_content = request.form.get('reply_email_content')
        if email_send_to_detail:
            new_email = Email(sent_to=email_send_to, sender=current_user.id, email_subject=email_subject,
                              email_content=email_content, email_status='inbox', email_time=datetime.now())
            db.session.add(new_email)
            db.session.commit()
            flash('Email sent successfully', 'success')
            return redirect(url_for('views.single_email', id=email_send_to_detail.id))
        else:
            flash('Email not found', 'danger')
            return redirect(url_for('views.single_email', id=email_send_to_detail.id))


@views.route("/forward_email_form/email:id<id>", methods=['GET', 'POST'])
@login_required
def forward_email_form(id):
    getting_email_detail = Email.query.filter(Email.id == id).first()
    if request.method == 'POST':
        email_send_to_detail = User.query.filter(User.email == request.form.get(
            'email_sent_to'), User.status == 'active').first()
        email_send_to = email_send_to_detail.id
        email_subject = getting_email_detail.email_subject
        email_content = request.form.get('forward_email_content')
        if email_send_to_detail:
            new_email = Email(sent_to=email_send_to, sender=current_user.id, email_subject=email_subject,
                              email_content=email_content, email_status='inbox', email_time=datetime.now())
            db.session.add(new_email)
            db.session.commit()
            flash('Email sent successfully', 'success')
            return redirect(url_for('views.single_email', id=email_send_to_detail.id))
        else:
            flash('Email not found', 'danger')
            return redirect(url_for('views.single_email', id=email_send_to_detail.id))


@views.route("/important_emails")
@login_required
def important_emails():
    getting_mail_details = Email.query.filter(Email.email_important == 'yes', Email.email_status ==
                                              'inbox', Email.sent_to == current_user.id).order_by(Email.email_time.desc()).all()
    temporary_sender_list = []
    sender_list = []
    for getting_emails_sender in getting_mail_details:
        temporary_sender_list.append(getting_emails_sender.sender)
    for temporary_sender_list in temporary_sender_list:
        sender_user_detail = User.query.filter(
            User.id == temporary_sender_list).all()
        for sender_user_detail in sender_user_detail:
            sender_list.append(sender_user_detail.email)
    return render_template("gmail_imp_email.html", getting_mail_details=getting_mail_details, sender_list=sender_list)


@views.route("/single_important_email/email_id:<id>", methods=['GET', 'POST'])
@login_required
def single_important_email(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id, Email.sent_to == current_user.id).first()
    getting_detail_of_sender = User.query.filter(
        User.id == getting_email_detail.sender).first()
    getting_email_detail.read_status = 'yes'
    db.session.commit()
    return render_template("gmail_single_important.html", getting_email_detail=getting_email_detail, getting_detail_of_sender=getting_detail_of_sender)


@views.route("/bin_email")
@login_required
def bin_email():
    getting_mail_details = Email.query.filter(
        Email.email_status == 'bin', Email.sent_to == current_user.id).order_by(Email.email_time.desc()).all()
    temporary_sender_list = []
    sender_list = []
    for getting_emails_sender in getting_mail_details:
        temporary_sender_list.append(getting_emails_sender.sender)
    for temporary_sender_list in temporary_sender_list:
        sender_user_detail = User.query.filter(
            User.id == temporary_sender_list).all()
        for sender_user_detail in sender_user_detail:
            sender_list.append(sender_user_detail.email)
    return render_template("gmail_bin_email.html", getting_mail_details=getting_mail_details, sender_list=sender_list)


@views.route("/starred")
@login_required
def starred():
    getting_mail_details = Email.query.filter(Email.email_star == 'yes', Email.email_status ==
                                              'inbox', Email.sent_to == current_user.id).order_by(Email.email_time.desc()).all()
    temporary_sender_list = []
    sender_list = []
    for getting_emails_sender in getting_mail_details:
        temporary_sender_list.append(getting_emails_sender.sender)
    for temporary_sender_list in temporary_sender_list:
        sender_user_detail = User.query.filter(
            User.id == temporary_sender_list).all()
        for sender_user_detail in sender_user_detail:
            sender_list.append(sender_user_detail.email)
    return render_template("gmail_starred.html", getting_mail_details=getting_mail_details, sender_list=sender_list)


@views.route("/single_starred_email/email_id:<id>", methods=['GET', 'POST'])
@login_required
def single_starred_email(id):
    getting_email_detail = Email.query.filter(
        Email.id == id, Email.sent_to == current_user.id).first()
    getting_detail_of_sender = User.query.filter(
        User.id == getting_email_detail.sender).first()
    getting_email_detail.read_status = 'yes'
    db.session.commit()
    return render_template("gmail_single_starred.html", getting_email_detail=getting_email_detail, getting_detail_of_sender=getting_detail_of_sender)


@views.route("/searchbar", methods=['GET', 'POST'])
@login_required
def searchbar():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_data']
        search = "%{}%".format(search_value)
        email_search = Email.query.filter(Email.email_subject.like(search) | Email.email_content.like(
            search), Email.email_status == 'inbox').order_by(Email.email_time.desc()).all()
        temporary_sender_list = []
        sender_list = []
        for getting_emails_sender in email_search:
            temporary_sender_list.append(getting_emails_sender.sender)
        for temporary_sender_list in temporary_sender_list:
            sender_user_detail = User.query.filter(
                User.id == temporary_sender_list).all()
            for sender_user_detail in sender_user_detail:
                sender_list.append(sender_user_detail.email)
            if form['search_data'] == "":
                return redirect(url_for('views.home'))
            else:
                return render_template('gmail_searchbar.html', email_search=email_search, sender_list=sender_list)
    return render_template('gmail_searchbar.html')
