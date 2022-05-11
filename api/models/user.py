import os

from flask import g
from datetime import datetime
from backend.api.db import db
from passlib.apps import custom_app_context as pwd_context
from ..utils.auth import auth, jwt
from itsdangerous import (BadSignature, SignatureExpired)


class User(db.Model):
    """ User Model for storing user details."""

    # The line below will override the "table name"
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    public_id = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(100), unique=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    gender = db.relationship("Gender", backref='user', lazy=True)
    role = db.relationship("Roles", backref='user', lazy=True)
    post = db.relationship("Post", backref='user', lazy=True)

    def hash_password(self, password_hash):
        self.password_hash = pwd_context.encrypt(password_hash)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, permission_level):
        if permission_level == 1:
            # Admin
            token = jwt.dumps({'id': self.id, "admin": 1})
            return token
        if permission_level == 2:
            # Super Admin
            token = jwt.dumps({'id': self.id, "admin": 2})
            return token
        else:
            # Normal user
            token = jwt.dumps({"id": self.id, "admin": 0, "email": self.email})
            return token

    # def generate_auth_token(self):
    #     token = jwt.dumps({'id': self.id, "email": self.email})
    #     return token

    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        g.user = None
        try:
            data = jwt.loads(token)
        except SignatureExpired:
            print("Signature expired")
            return None  # valid token but expired
        except BadSignature:
            print("Bad Signature")
            return None  # invalid token
        if "email" and "admin" in data:
            g.user = data["email"]
            g.admin = data["admin"]
            return True
        return False

    @staticmethod
    @auth.get_user_roles
    def get_user_roles(user):
        return user.get_roles()

    def __repr__(self):
        return f"User: email-> {self.username}, user id -> {self.id}, date created -> {self.registered_on}"


class Blacklist(db.Model):
    """A list of invalid refresh tokens"""

    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(length=255))

    def __repr__(self):
        return "<User(id='%s', refresh_token='%s', status='invalidated.')>" % (
            self.id,
            self.refresh_token,
        )


class Department(db.Model):
    """A collection of all departments within school."""

    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.id'), nullable=True)

    def __repr__(self):
        return f"Department {self.department_name}"


def get_department():
    return Department.query


class EducationLevel(db.Model):
    """A collection of all education levels i.e undergraduate, post graduate, doctorate."""

    id = db.Column(db.Integer, primary_key=True)
    education = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    def __repr__(self):
        return f"Education level ('{self.education}')"


def get_education():
    return EducationLevel.query


class Major(db.Model):
    """A collection of all majors ranging from undergraduate, post graduate to doctorate levels"""

    id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    def __repr__(self):
        return f"Major {self.major}"


def get_major():
    return Major.query.all()


class Roles(db.Model):
    """User Roles include: admin, student, supervisor(lecturer & research officer) and """

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default="user", nullable=False)  # unless specified, default user is user
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Roles('{self.title}')"


def get_role():
    return Roles.query


class Gender(db.Model):
    """A collection of the gender, i.e male, female & other."""
    __tablename__ = "gender"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Gender('{self.gender}')"


def get_gender():
    return Gender.query


class Student(db.Model):
    """Students details"""

    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    research_topic = db.Column(db.String(250), nullable=False)
    education_level = db.relationship("EducationLevel", backref='student', lazy=True)
    department = db.relationship("Department", backref='student', lazy=True)
    major = db.relationship("Major", backref='student', lazy=True)
    supervisor = db.relationship("Supervisor", backref='student', lazy=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    def __repr__(self):
        data = {"research_topic": self.research_topic, "education_level": self.education_level,
                "department": self.department}
        return f"Student('{data}')"


def get_students():
    return Student.query


class Supervisor(db.Model):
    """Supervisor Model."""
    __tablename__ = "supervisor"
    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(250), nullable=False)
    department = db.relationship("Department", backref='supervisor', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    def __repr__(self):
        return f"Supervisor('{self.specialization}')"


def get_supervisor():
    return Supervisor.query
