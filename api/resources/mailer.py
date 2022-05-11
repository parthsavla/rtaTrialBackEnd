from flask import request, jsonify, g, make_response
from flask_restful import Resource, abort, reqparse
from ..utils.auth import auth
from ..utils import role_required
from backend.api.db import db
from ..utils.exceptions import MailException
from ..utils.mailer import (research_notification, pdf_template,
                            reject_notification, accept_notification)
from ..models.mailpost import Post
from ..models.user import (User, EducationLevel, Major)


class Notification(Resource):
    """Api for general notifications to all users in the system,
    important for crucial communication from research office."""

    @auth.login_required
    def post(self):
        """
        @:param: content, user_mails, etc.
        :return:
        """
        data = request.get_json()
        return jsonify({"status": "General mailer for notifications."})


class MailSupervisor(Resource):
    """Api to send mail from student to supervisor, requesting for approval so as to partake
    in data collection."""

    @auth.login_required
    @role_required.permission(0)
    def get(self):
        return jsonify({"email": "supervisor email"})

    @staticmethod
    @auth.login_required
    @role_required.permission(0)
    def post():
        try:
            data = request.get_json()
            user_details = User.query.filter_by(id=g.user['id']).first()
            student_email = user_details.email
            supervisor_mail = data["supervisor_mail"]
            mail_post = Post(title=data["title"], content=data["content"])

            education = EducationLevel.query.filter_by(education=data["education"])
            major = Major.query.filter_by(major=data["major"])
            user = User()

            if education:
                education = EducationLevel(education=data["education"])
            else:
                pass

            if major:
                major = Major(major=data["major"])
            else:
                pass

            db.session.add(mail_post)
            mail_post.major.append(major)
            mail_post.education.append(education)
            db.session.add(user)
            db.session.commit()

            research_notification(student_email, supervisor_mail)
            res = jsonify({"msg": "Mail Send Successfully to Supervisor"})
            return make_response(res, 200)
        except MailException as mailing_error:
            exception_error = jsonify({"Error Message": mailing_error})
            return make_response(exception_error, 404)


class MailStudent(Resource):
    """Api to respond to student with a success or failure message.
    - Success message means the student is able to download a letter while,
    failure message means the student has to do extra assignment to and try letter."""

    @auth.login_required
    @role_required.permission(0)
    def get(self):
        pass

    @staticmethod
    @auth.login_required
    def post():
        try:
            data = request.get_json()
            user = g.user
            receiver_mail = data["receiver_mail"]
            research_notification(user, receiver_mail)
            res = jsonify({"status": "Send mail to supervisor"})
            return make_response(res, 200)
        except MailException as mailing_error:
            error = jsonify({"status": mailing_error})
            return make_response(error, 404)

