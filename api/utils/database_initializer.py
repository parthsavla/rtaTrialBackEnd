#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from ..db import db
from flask import g
from ..models.user import (User, Major, EducationLevel as Education,
                           Gender, Roles, Supervisor, Blacklist, Department, Student)
from ..models.mailpost import Post


def create_super_admin():
    user = User.query.filter_by(username="sa_username").first()
    if user is None:
        # create admin if one does not exist
        user = User(username="sa_username", email="sa_email@example.com", password="sa_password")
        db.session.add(user)
        db.session.commit()
        logging.info("Super admin created.")
        return user
    else:
        logging.info("Super admin already exist.")
        return


def create_admin_user():
    user = User.query.filter_by(email="admin_email@example.com").first()
    if user is None:
        user = User(
            username="admin_username",
            password_hash="admin_password",
            email="admin_email@example.com"
        )
        db.session.add(user)
        db.session.commit()
        logging.info("Admin created.")
        return user
    else:
        logging.info("Admin already exist.")
        return


def create_test_user():
    user = User.query.filter_by(email="test_email@example.com")
    password = "test_password"
    email = "test_email@example.com"

    if user is None:
        user = User(
            username="test_username",
            password_hash=password,
            email=email
        )
        db.session.add(user)
        db.session.commit()
        logging.info("Test User created.")
        return user
    else:
        logging.info("Test User already exist.")
        return


def create_gender():
    male_gender = Gender(gender='Male')
    female_gender = Gender(gender='Female')
    other_gender = Gender(gender='Other')
    db.session.add(male_gender)
    db.session.add(female_gender)
    db.session.add(other_gender)
    db.session.commit()


print('Successfully created gender')


def create_role():
    admin_role = Roles(title='Admin', description='Administrative roles')
    student_role = Roles(title='Student', description='Student in need of an Ok.')
    supervisor_role = Roles(title='Supervisor', description='Supervises the research.')
    db.session.add(admin_role)
    db.session.add(student_role)
    db.session.add(supervisor_role)
    db.session.commit()


def create_post():
    post_1 = Post(title='Some Title', content='Administrative roles are cool')
    user = User()
    db.session.add(post_1)
    db.session.add(user)
    # post_1.user_id.append(g.get("id"))
    db.session.commit()


print('Successfully created post table')


def create_major():
    major1 = Major(major='B.Sc. Accounting', user_id=1)
    major2 = Major(major='B.Sc. Finance', user_id=1)
    major3 = Major(major='B.Sc. Hotel and Restraurant Management', user_id=1)
    major4 = Major(major='B.Sc. International Business Administration', user_id=1)
    major5 = Major(major='Master of Science in Management & Organizational Development', user_id=1)
    major6 = Major(major='Master of Business Administration', user_id=1)
    major7 = Major(major='Doctor of Business Administration', user_id=1)
    major8 = Major(major='B.A Animation', user_id=1)
    major9 = Major(major='B.A Film Production & Directing', user_id=1)
    major10 = Major(major='B.A Journalism', user_id=1)
    major11 = Major(major='M.A. Communication Studies', user_id=1)
    major12 = Major(major='B.A. Criminal Justice',user_id=1)
    major13 = Major(major='B.A International Relations', user_id=1)
    major14 = Major(major='B.A. Psychology', user_id=1)
    major15 = Major(major='M.A. Clinical Psychology', user_id=1)
    major16 = Major(major='M.A. Counselling Psychology',user_id=1)
    major17 = Major(major='M.A. International Relations', user_id=1)
    major18 = Major(major='M.A. Marriage & Family Therapy',user_id=1)
    major19 = Major(major='Doctor of Philosophy in International Relations',user_id=1)
    major20 = Major(major='Doctor of Psychology(Psy.D), Clinical Psychology',user_id=1)
    major21 = Major(major='B.Sc. Applied Computer Technology',user_id=1)
    major22 = Major(major='B.Sc. Information Systems and Technology', user_id=1)
    major23 = Major(major='Doctor of Philosophy, Information Systems & Technology', user_id=1)
    major24 = Major(major='Bachelor of Pharmacy', user_id=1)
    major25 = Major(major='B.Sc. Epidermology & Biostatics', user_id=1)
    major_list = [major25, major24, major23, major22, major21, major20, major19, major18, major17, major16, major15,
                  major14, major13, major12, major11, major10, major9, major8, major7, major6, major5, major4, major3,
                  major2, major1]
    for i in major_list:
        db.session.add(i)
    db.session.commit()


print('Successfully created major')


def create_education():
    undergrad = Education(education='Undergraduate')
    graduate = Education(education='Graduate')
    doctoral = Education(education='Doctoral')
    db.session.add(undergrad)
    db.session.add(graduate)
    db.session.add(doctoral)
    db.session.commit()


print('Successfully created education!')


def create_student():
    student1 = Student(research_topic='My Undergrad Undergraduate Topic')
    db.session.add(student1)
    db.session.commit()


print('Successfully created student!')


def create_supervisor():
    undergrad = Supervisor(specialization='Undergraduate Students', department="ICT")
    graduate = Supervisor(specialization='Graduate Students', department="ICT")
    doctoral = Supervisor(specialization='Doctoral Students', department="ICT")
    db.session.add(undergrad)
    db.session.add(graduate)
    db.session.add(doctoral)
    db.session.commit()


print('Successfully created supervisor!')

print('Finished populating the db accordingly')
