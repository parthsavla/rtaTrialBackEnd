#!flask/bin/python
import logging

from flask import jsonify, request, g, json, make_response, url_for, abort
from sqlalchemy import func
from flask_restful import Resource
from backend.api.db import db
from ..utils.errors import (SERVER_ERROR_500, DOES_NOT_EXIST, NOT_ADMIN, UNAUTHORIZED, NOT_FOUND_404, NO_INPUT_400,
                            INVALID_INPUT_422, ALREADY_EXIST)
from ..models.user import (User, Blacklist, Roles)
from ..utils.exceptions import DatabaseError
from ..utils.auth import auth, refresh_jwt
from ..utils import role_required


class IndexApi(Resource):
    """Home page"""

    def __init__(self):
        pass

    @staticmethod
    @auth.login_required
    @role_required.permission(0)
    def get():
        data = jsonify({"home": "Research Application API resource.", "user": g.user})
        return make_response(data, 200)


class RegisterApi(Resource):
    """A resource for creating a new user resource."""

    @staticmethod
    def post():
        try:
            user_data = request.get_json()
            username = user_data['username'].strip()
            password = user_data['password'].strip()
            email = user_data['email'].strip()
        except Exception as e:
            logging.info(f'Error: {e}')
            error_msg = json.dumps({'error': e})
            return make_response(error_msg, 403)

        if username is None or password is None:
            return INVALID_INPUT_422  # Invalid user input

        if User.query.filter_by(username=username).first() is not None:
            return ALREADY_EXIST  # Already existing user. error 409

        try:
            user = User(email=email, username=username)
            user.hash_password(password)
            db.session.add(user)
            role = Roles(title="user", description="default user")
            user.role.append(role)
            db.session.commit()
            data = jsonify({"msg": "Registration successful, proceed to login and setup your profile"},
                           {"id": str(user.id), "username": user.username, "email": user.email})
            return make_response(data, 201)
        except DatabaseError as e:
            message = json.dumps({'errors': e})
            return make_response(message, 400)

    def patch(self, user_id, username, email, first_name, last_name, public_id, gender, role):
        user_data = User.query.filter_by(id=user_id).one()
        if user_data:
            try:
                if not email:
                    user_data.email = email
                if not username:
                    user_data.username = username
                if not first_name:
                    user_data.first_name = first_name
                if not last_name:
                    user_data.last_name = last_name
                if not public_id:
                    user_data.public_id = public_id
                if not gender:
                    user_data.gender = public_id
                if not role or user_data.role == "user":
                    user_data.role = role
                if user_data.role == "admin" or user_data.role == "super_admin":
                    # We don't want the user to give themselves admin rights
                    # because this route is open for all
                    # TODO: Create a special route for admin/super admit edits
                    abort(403)

                db.session.add(user_data)
                db.session.commit()
                res = jsonify({"msg": f'User with id {user_id} updated successfully!'})
                return make_response(res, 204)
            except Exception as e:
                logging.info(e)
                message = json.dumps({'errors': e})
                return make_response(message, 500)
        else:
            res = jsonify({"msg": f'User with ID: {user_id} does not exist!'})
            return make_response(res, 404)


class LoginApi(Resource):
    """Managing login into the application."""

    def __init__(self):
        pass

    @staticmethod
    def post():
        user_data = request.get_json()
        username = user_data['username']
        password = user_data['password']

        if username is None and password is None:
            res = jsonify({"msg": "Enter username or password again"})
            return make_response(res, 400)

        user = User.query.filter_by(username=username).first()
        if user is None:
            res = jsonify({"msg": "Please register first OR check your username"})
            return make_response(res, 403)

        if user.verify_password(password):
            try:
                role = Roles.query.filter_by(user_id=user.id).first()
                token = None
                if role.title == "user":
                    token = user.generate_auth_token(0)
                elif role.title == "admin":
                    token = user.generate_auth_token(1)
                elif role.title == "super admin":
                    token = user.generate_auth_token(2)

                refresh_token = refresh_jwt.dumps({"id": user.id, "email": user.email, "admin": role.title})
                res = jsonify({'msg': 'user successfully logged in.'},
                              {"user_id": user.id, "username": user.username,
                               "user_role": role.title, "email": user.email},
                              {"access_token": token.decode(), "refresh_token": refresh_token.decode()})
                return make_response(res, 200)
            except Exception as e:
                logging.info(e)
                res = jsonify({"msg": "Unauthorized access."})
                return make_response(res, DOES_NOT_EXIST)
        else:
            res = jsonify({'msg': 'authentication failed. Check username and/or password'})
            return make_response(res, 401)


class LogoutApi(Resource):
    """API to sign out of the application."""

    @staticmethod
    @auth.login_required
    def post():
        refresh_token = request.json.get("refresh_token")
        # confirm if the refresh token is in the blacklist
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()

        if ref is not None:
            res = jsonify({"status": "Already invalidated", "refresh_token": refresh_token})
            return make_response(res, 403)

        # Otherwise, create a blacklist of the existing refresh_token
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token)
        db.session.add(blacklist_refresh_token)
        db.session.commit()
        res = jsonify({"status": "Invalidated", "expired_token": refresh_token})
        return make_response(res, 200)


class RefreshToken(Resource):
    """Api to generate a refresh token."""

    @staticmethod
    def post():
        refresh_token = request.json.get("refresh_token")
        # Confirm if the refresh token is blacklisted
        ref = Blacklist.query.filter_by(refresh_token=refresh_token)
        if ref:
            res = jsonify({"status": "Token Invalidated"})
            return make_response(res, 403)
        # otherwise, we generate new token
        try:
            new_token = refresh_jwt.loads(refresh_token)
        except Exception as token_exception:
            logging.error(token_exception)
            res = jsonify({"status": False, "msg": "Token generation failed."})
            return make_response(res, 500)

        # Otherwise, create new user to re-generate token
        user = User(email=new_token["email"])
        # refresh_token = user.generate_auth_token(False)
        refresh_token = user.generate_auth_token()
        token = jsonify({"access_token": refresh_token})
        return make_response(token, 201)


class ResetPassword(Resource):
    """Api to reset password"""

    @auth.login_required
    def put(self):
        # get the old and new password first
        old_pwd, new_pwd = request.json.get("old_pwd"), request.json.get("new_pwd")
        user = User.query.filter_by(email=g.user).first()

        # confirm user & that the user old pwd matches with the existing
        if not user and not user.verify_password(old_pwd):
            res = jsonify({"msg": "your old password does not match"})
            return make_response(res, UNAUTHORIZED)
        user.hash_password(new_pwd)
        db.session.commit()
        res = jsonify({"msg": "New password set successfully"})
        return make_response(res, 201)


class DataUser(Resource):
    """Normal user API calls."""
    def __init__(self):
        pass

    @auth.login_required
    @role_required.permission(0)
    def get(self):
        user_id = request.args.get("user_id")
        data = list()
        if user_id:
            user = User.query.filter_by(id=int(user_id)).first()
            if user:
                data.append({"user_id": user.id, "email": user.email, "username": user.username,
                             "date_registered": user.registered_on})
            res_data = jsonify({"user_data": data, "msg": "User Data fetched successful"})
            return make_response(res_data, 200)
        res = jsonify({"msg": NOT_FOUND_404})
        return make_response(res, 400)


class DataAdmin(Resource):
    """Admin  API calls"""

    @staticmethod
    @auth.login_required
    @role_required.permission(1)
    def get():
        # get users
        # start_date = datetime.strptime(data["start_date"], "%d.%m.%Y")
        return {'user': "Just admin"}


class DataSuperAdmin(Resource):
    """Super Admin API calls"""

    @staticmethod
    @auth.login_required
    @role_required.permission(2)
    def get():
        # get user
        return {'user': "super admin"}


class AdminApi(Resource):
    """For admin dashboard api calls"""

    # get all users
    @staticmethod
    @auth.login_required
    @role_required.permission(0)
    def get():
        users = User.query.all()
        users_details = []
        for user in users:
            users_details.append((user.username, user.email, user.registered_on))
        if not users_details:
            return make_response(jsonify({"msg": "Admin user does not exist!"}), 404)
        data = jsonify({"users": users_details})
        return make_response(data, 200)


class UserMetrics(Resource):
    # Get the number of registered users
    @staticmethod
    @auth.login_required
    @role_required.permission(1)
    def get():
        num = db.session.query(func.count(User.id)).scalar()
        data = jsonify({"users_num": num})
        return make_response(data, 200)
