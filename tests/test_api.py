from unittest import TestCase
import json
import re
from base64 import b64encode
from .. import create_app, db
# Models
from ..api.models.user import User
from ..api.models.mailpost import Post


class TestAuthentication(TestCase):
    """Test case for all authentication API endpoints"""

    def setUp(self):
        self.app = create_app('tests').test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_signup(self):
        """
        Test the signup route.
        :return:
        """