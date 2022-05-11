import os
import unittest

from flask import current_app
from .. import create_app, db
from backend.config import basedir


class TestDevelopmentConfig(unittest.TestCase):
    def setUp(self):

        self.app = create_app('dev')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_is_development(self):
        self.assertFalse(self.app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, './storage/research_main.db')
        )


class TestTestingConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('tests')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_is_testing(self):
        self.assertFalse(self.app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, './storage/research_test.db')
        )


class TestProductionConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('prod')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_is_production(self):
        self.assertTrue(self.app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
