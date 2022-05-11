"""'
Handles the forms send back and forth.
"""

import os
from itsdangerous import (SignatureExpired, BadSignature)
from ..utils.auth import auth, jwt
from datetime import datetime
from flask import g
from ... import db


class Post(db.Model):
    """This is a model for all the mail posts exchanges between the student
    and the supervisor."""

    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(100), default="pending")
    supervisor = db.relationship("Supervisor", backref='post', lazy=True)
    student = db.relationship("Student", backref='post', lazy=True)
    major = db.relationship("Major", backref='post', lazy=True)
    education = db.relationship("EducationLevel", backref='post', lazy=True)

    # We can generate token that expires after three months for the research mail confirm links below.
    def get_mail_token(self, expires_sec=7.884e+6):
        s = jwt(expires_in=expires_sec)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    @auth.verify_token
    def verify_mail_token(token):
        g.user = None
        try:
            user = jwt.loads(token)
        except SignatureExpired:
            return None  # Expired Token
        except BadSignature:
            return None  # invalid token
        # user = Post.query.filter_by(user_id=user_id.get('id')).first()
        if user:
            g.user = user
            return True
        return False

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.supervisor_name}')"
