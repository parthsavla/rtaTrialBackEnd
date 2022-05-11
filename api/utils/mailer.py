import os
import secrets
import pdfkit
import datetime
from PIL import Image
from flask import url_for, render_template, current_app, make_response, g
from flask_mail import Message
from .decorators import asynco
from ...config import Config
from threading import Thread
from ...api.models.user import User, Roles
from ...api.models.mailpost import Post
from flask_mail import Mail

mail = Mail()


# For saving pictures if necessary.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# For resetting emails.
# TODO: Add async mailing functionality. Very important.
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


# We want to do mail send and receiving down below:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    app = g.user  # current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()


def research_notification(user, mail_receiver):
    # User post right here.
    all_user_posts = Post.query.filter_by(user_id=g.user["id"]).all()
    # user_details = all_user_posts[-1]
    user_details = all_user_posts[-1]
    # Token here
    token_user = Post.query.filter_by(supervisor_email=mail_receiver).first()
    token = token_user.get_mail_token()
    # user details to fill in the form.
    # user_data = Post.query.get(token_user)
    return send_email("Your student sent you a mail.!",
                      user,
                      [mail_receiver],
                      render_template("send_supervisor.html", token=token, user_details=user_details))


def accept_notification(user, mail_receiver):
    # Token here
    token_user = User.query.filter_by(email=user).first()
    p_user = Post.query.filter_by(user_id=token_user.id).first()
    token = p_user.get_mail_token()
    return send_email("Your supervisor send you a success mail.!",
                      mail_receiver,
                      [user],
                      render_template("supervisor_succres.html", token=token))


def reject_notification(user, mail_receiver):
    return send_email("Your supervisor send you a rejection mail.!",
                      mail_receiver,
                      [user],
                      render_template("supervisor_failresp.html"))


# We generate pdf letter by converting it from the html below.
def pdf_template(user):
    user_name = user
    date = datetime.datetime.now().strftime('%d %B , %Y')
    user_details = Post.query.filter_by(user_id=user.id).all()
    rendered = render_template('letterPdf.html', user_details=user_details[-1],
                               User_name=user_name, date=date)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'no-outline': None
    }
    # css = [os.path.join(Config.ABS_PATH_STATIC_FOLDER, 'style.css')]
    # img = [os.path.join(Config.ABS_PATH_STATIC_FOLDER, '/mail_pics/usiu_mail1.png')]
    pdf = pdfkit.from_string(rendered, False, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=letter.pdf'
    return response
