#!flask/bin/python
import logging

from datetime import datetime
from flask import jsonify, abort, request, g, url_for, json, make_response
from sqlalchemy import func
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from backend.api.db import db
from ..utils.errors import (SERVER_ERROR_500, DOES_NOT_EXIST, NOT_ADMIN, UNAUTHORIZED, NOT_FOUND_404, NO_INPUT_400,
                            INVALID_INPUT_422, ALREADY_EXIST)
from ..models.user import (User, Blacklist, EducationLevel, Department, Major, Student)
from ..models.user import (get_education, get_major)
from ..utils.exceptions import DatabaseError
from ..utils.auth import auth, refresh_jwt
from ..utils import role_required


class ManageEducation(Resource):
    def __init__(self):
        pass

    def get(self):
        education = EducationLevel.query.all()
        education_details = []
        for education_level in education:
            education_details.append(education_level.education)
        if not education_details:
            return make_response(jsonify({"msg": "Education level does not exist!"}), 404)
        data = jsonify({"education_level": education_details})
        return make_response(data, 200)

    def post(self):
        try:
            data = request.get_json()
            education = data['education'].strip()
        except Exception as e:
            logging.info(f'Error: {e}')
            error_msg = json.dumps({'error': e})
            return make_response(error_msg, 403)

        if data is None or education is None:
            return INVALID_INPUT_422  # Invalid user input

        if EducationLevel.query.filter_by(education=education).first() is not None:
            return ALREADY_EXIST  # Already existing user. error 409

        try:
            education = EducationLevel(education=education)
            db.session.add(education)
            db.session.commit()
            data = jsonify({"msg": "Education level added successfully"},
                           {"education": education.education})
            return make_response(data, 201)
        except DatabaseError as e:
            message = json.dumps({'errors': e})
            return make_response(message, 400)

    def put(self):
        # Edit the education level
        education_level = request.json.get("education_level")
        education = EducationLevel.query.filter_by(education=education_level).first()

        # confirm education level existence
        if not education_level and not education:
            res = jsonify({"msg": "Education level does not exist"})
            return make_response(res, UNAUTHORIZED)
        db.session.commit()
        res = jsonify({"msg": "Education level changed successfully"})
        return make_response(res, 201)

    def patch(self):
        user_data = request.get_json()
        edu_id = user_data["edu_id"]
        education = user_data["education"]
        education_data = EducationLevel.query.filter_by(id=edu_id).one()
        if education_data:
            try:
                user_data.education = education
                db.session.add(user_data)
                db.session.commit()
                res = jsonify({"msg": f'Education resource with id {edu_id} updated successfully!'})
                return make_response(res, 204)
            except DatabaseError as e:
                logging.info(e)
                message = json.dumps({'errors': e})
                return make_response(message, 500)
        else:
            pass

    def delete(self, edu_id):
        try:
            education_to_delete = Major.query.filter_by(edu_id)
            db.session.delete(education_to_delete)
            db.session.commit()
            res = jsonify({"msg": f'Department resource of id {edu_id} DELETED!'})
            return make_response(res, 204)
        except DatabaseError as e:
            logging.info(e)
            res = jsonify({"error": e})
            return make_response(res, SERVER_ERROR_500)


class ManageDepartment(Resource):
    def __init__(self):
        pass

    def get(self):
        department = Department.query.all()
        departments = []
        if not departments:
            return make_response(jsonify({"msg": "Department does not exist!"}), 404)
        for department in department:
            departments.append(department.department_name)
        data = jsonify({"education_level": departments})
        return make_response(data, 200)

    def post(self):
        try:
            data = request.get_json()
            department = data['department'].strip()
        except Exception as e:
            logging.info(f'Error: {e}')
            error_msg = json.dumps({'error': e})
            return make_response(error_msg, 403)

        if data is None or department is None:
            return INVALID_INPUT_422  # Invalid user input

        if Department.query.filter_by(department_name=department).first() is not None:
            return ALREADY_EXIST  # Already existing department. error 409

        try:
            new_department = Department(department_name=department)
            db.session.add(new_department)  # Add user.id later to denote whoever made changes
            db.session.commit()
            data = jsonify({"msg": "New Department added successfully"},
                           {"department": new_department.department_name})
            return make_response(data, 201)
        except DatabaseError as e:
            message = json.dumps({'errors': e})
            return make_response(message, 400)

    def patch(self):
        dep_data = request.get_json()
        dep_id = dep_data["department_id"]
        dep_name = dep_data["department_name"]
        dep_data = EducationLevel.query.filter_by(id=dep_id).one()
        if dep_data:
            try:
                dep_data.department_name = dep_name
                db.session.add(dep_data)
                db.session.commit()
                res = jsonify({"msg": f'Department resource with id {dep_id} updated successfully!'})
                return make_response(res, 204)
            except DatabaseError as e:
                logging.info(e)
                message = json.dumps({'errors': e})
                return make_response(message, SERVER_ERROR_500)
        else:
            pass

    def put(self):
        # Edit the education level
        department = request.json.get("department")
        department_to_replace = EducationLevel.query.filter_by(department_name=department).first()

        # confirm education level existence
        if not department and not department_to_replace:
            res = jsonify({"msg": "Department name does not exist"})
            return make_response(res, UNAUTHORIZED)
        db.session.commit()
        res = jsonify({"msg": "Department replaced successfully"})
        return make_response(res, 201)

    def delete(self, dep_id):
        try:
            department_to_delete = Major.query.filter_by(dep_id)
            db.session.delete(department_to_delete)
            db.session.commit()
            res = jsonify({"msg": f'Department resource of id {dep_id} DELETED!'})
            return make_response(res, 204)
        except DatabaseError as e:
            logging.info(e)
            res = jsonify({"error": e})
            return make_response(res, SERVER_ERROR_500)


class ManageMajor(Resource):

    def __init__(self):
        pass

    @staticmethod
    @auth.login_required
    def get():
        try:
            major_collection = [i for i in get_major()]

            if not major_collection:
                return make_response(jsonify({"msg": "Major does not exist!"}), 404)
            data = jsonify({"major_list": str(major_collection)})
            return make_response(data, 200)
        except Exception as e:
            res = jsonify({"Error_Message": str(e)})
            return make_response(res, 500)

    @auth.login_required
    @role_required.permission(0)  # TODO: change to ADMIN/SUPER ADMIN Permission
    def post(self):
        try:
            data = request.get_json()
            major = data['major'].strip()
        except Exception as e:
            logging.info(f'Error: {e}')
            error_msg = json.dumps({'error': e})
            return make_response(error_msg, 403)

        if data is None or major is None:
            return INVALID_INPUT_422  # Invalid user input

        if Major.query.filter_by(major=major).first() is not None:
            return ALREADY_EXIST  # Already existing department. error 409

        try:
            new_major = Major(major=major)
            db.session.add(new_major)  # Add user.id later to denote whoever made changes
            db.session.commit()
            data = jsonify({"msg": "New Department added successfully"},
                           {"department": new_major.major})
            return make_response(data, 201)
        except DatabaseError as e:
            message = json.dumps({'errors': e})
            return make_response(message, 400)

    def patch(self):
        education_data = EducationLevel.query.filter_by(id=edu_id).one()
        if education_data:
            try:
                pass
            except DatabaseError as e:
                logging.info(e)
                message = json.dumps({'errors': e})
                return make_response(message, 500)
        else:
            pass

    def put(self):
        pass

    def delete(self, major_id):
        try:
            major_to_delete = Major.query.filter_by(major_id)
            db.session.delete(major_to_delete)
            db.session.commit()
            res = jsonify({"msg": f'Major resource of id {major_id} DELETED!'})
            return make_response(res, 204)
        except DatabaseError as e:
            logging.info(e)
            res = jsonify({"error": e})
            return make_response(res, 500)


class StudentApi(Resource):

    def __init__(self):
        pass

    def get(self, stud_id):
        student = Student.query.filter_by(id=stud_id)
        student_details = []
        for student_item in student:
            student_details.append(student_item.education_level)
        if not student_details:
            return make_response(jsonify({"msg": "Student does not exist!"}), 404)
        data = jsonify({"education_level": student_details})
        return make_response(data, 200)

    def post(self):
        pass

    def patch(self):
        education_data = EducationLevel.query.filter_by(id=edu_id).one()
        if education_data:
            try:
                pass
            except DatabaseError as e:
                logging.info(e)
                message = json.dumps({'errors': e})
                return make_response(message, 500)
        else:
            pass

    def put(self):
        pass

    def delete(self, student_id):
        try:
            student_to_delete = Major.query.filter_by(student_id)
            db.session.delete(student_to_delete)
            db.session.commit()
            res = jsonify({"msg": f'Major resource of id {student_id} DELETED!'})
            return make_response(res, 204)
        except DatabaseError as e:
            logging.info(e)
            res = jsonify({"error": e})
            return make_response(res, 500)


class SupervisorApi(Resource):

    def __init__(self):
        pass

    def get(self):
        data = jsonify({"home": "Research Application API resource."})
        return make_response(data, 200)

    def post(self):
        pass

    def patch(self):
        education_data = EducationLevel.query.filter_by(id=edu_id).one()
        if education_data:
            try:
                pass
            except DatabaseError as e:
                logging.info(e)
                message = json.dumps({'errors': e})
                return make_response(message, 500)
        else:
            pass

    def put(self):
        pass

    def delete(self, supervisor_id):
        try:
            supervisor_to_delete = Major.query.filter_by(supervisor_id)
            db.session.delete(supervisor_to_delete)
            db.session.commit()
            res = jsonify({"msg": f'Supervisor resource of id {supervisor_id} DELETED!'})
            return make_response(res, 204)
        except DatabaseError as e:
            logging.info(e)
            res = jsonify({"error": e})
            return make_response(res, 500)
