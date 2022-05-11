"""
General configuration of the application done right here.
"""
import os
import json
import logging

from os import path
from sys import platform
from dotenv import load_dotenv

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# You have to create your own credentials for testing purposes and point the
# program to the right folder.
# Credentials include: email address, password, secret-key, database uri,

try:
    with open("C:/etc/resconfig.json") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    try:
        with open('/etc/resconfig.json') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        logging.error("File resconfig.json does not exist.")
finally:
    pass


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    FLASK_ENV = os.getenv('FLASK_ENV')
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_SUPPRESS_SEND = False
    MAIL_DEFAULT_SENDER = 'usiu.research.extension@gmail.com'
    MAIL_USERNAME = config.get('EMAIL_USER')
    MAIL_PASSWORD = config.get('EMAIL_PASS')
    TESTING = True
    HOST = '0.0.0.0'
    ABS_PATH_STATIC_FOLDER = "backend/api/utils/static"  # for css pdf-converter
    # Administrator List
    ADMINS = ['xogi@simplemail.top', 'usiu.research.extension@gmail.com']


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    Config.DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'research_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, './storage/research_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict({
    "dev": DevelopmentConfig(),
    "test": TestingConfig(),
    "prod": ProductionConfig()
}
)

key = Config.SECRET_KEY
