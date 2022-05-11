r"""
We are using Application Factories:
    - Using this design pattern, no application specific state is stored on the extension object,
    one extension object can be used for multiple apps.
    - This facilitates the ease at which we switch between development, testing and production environment
    by calling the create_app function.
"""
import os

from flask import Flask
from flask_bcrypt import Bcrypt
# from flask_swagger import swagger
from backend.api.db import db
from backend.config import config_by_name
from flask_migrate import Migrate
from flask_mail import Mail
from .api.utils.mailer import mail
from .api.resources.create_routes import initialize_routes
from .api.utils.database_initializer import (create_super_admin, create_admin_user, create_test_user,
                                             create_student, create_supervisor, create_education,
                                             create_role, create_major, create_gender, create_post)

# Set-up the middlewares
migrate = Migrate()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    flask_bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # generate routes
    initialize_routes(app)

    # check if there is no database, if so create
    if not os.path.exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        db.app = app  # new db app if no database
        db.create_all()  # Create all db tables
        # Create users (super admin, admin and test user)
        # create_super_admin()
        # create_admin_user()
        # create_test_user()
        # create_post()
        # create_major()
        # create_gender()
        # create_education()
        # create_supervisor()

    # Setup swagger for APIs tests.
    # app.config['SWAGGER'] = {
    #     'title': 'Research App APIs'
    # }
    # swagger(app)

    return app
