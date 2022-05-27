# write tests for the authentication module
from flask import Response
import pytest


def test_authentication_module_exists():
    """
    Test that the authentication module exists
    """
    import nuclei.authentication

    assert nuclei.authentication


def test_authentication_module_has_login_function():
    """
    Test that the authentication module has a login function
    """
    import nuclei.authentication

    assert nuclei.authentication.login


def test_authentication_module_has_logout_function():
    """
    Test that the authentication module has a logout function
    """
    import nuclei.authentication

    assert nuclei.authentication.logout


def test_authentication_module_has_login_required_decorator():
    """
    Test that the authentication module has a login required decorator
    """
    import nuclei.authentication

    assert nuclei.authentication.login_required


class TestAuthenticationModule:
    """
    Test the authentication module
    """

    def test_login_function_exists(self):
        """
        Test that the login function exists
        """
        import nuclei.authentication

        assert nuclei.authentication.login

    def test_login_function_returns_response(self):
        """
        Test that the login function returns a response
        """
        import nuclei.authentication

        assert nuclei.authentication.login() == Response

    def test_login_function_returns_response_with_status_code_200(self):
        """
        Test that the login function returns a response with status code 200
        """
        import nuclei.authentication

        assert nuclei.authentication.login().status_code == 200

    def test_login_function_returns_response_with_status_code_401(self):
        """
        Test that the login function returns a response with status code 401
        """
        import nuclei.authentication

        assert nuclei.authentication.login().status_code == 401

    def test_login_function_returns_response_with_content_type_html(self):
        """
        Test that the login function returns a response with content type html
        """
        import nuclei.authentication

        assert nuclei.authentication.login().content_type == "text/html"

    def test_login_function_returns_response_with_content_type_html(self):
        """
        Test that the login function returns a response with content type html
        """
        import nuclei.authentication

        assert nuclei.authentication.login().content_type == "text/html"
