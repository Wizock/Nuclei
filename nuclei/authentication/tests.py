import unittest

from .models import *
# write tests for the authentication module
from .views import *


class TestAuthentication(unittest.TestCase):
    # write tests for testing authentication
    def test_login_view(self):
        # test login view
        response = login({"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 200)
