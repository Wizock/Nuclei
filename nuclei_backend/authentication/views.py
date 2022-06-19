from __future__ import annotations

from calendar import c
from typing import *

import flask_praetorian
import werkzeug
from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_cors import cross_origin
from flask_login import current_user, login_required, login_user, logout_user
from flask_praetorian import auth_required, current_user, roles_accepted
from typing_extensions import *

auth = Blueprint(
    "authentication", __name__, template_folder="templates", url_prefix="/auth"
)

from ..extension_globals.database import db
from ..extension_globals.praetorian import guard
from .models import User


@auth.before_request
def make_session_permanent():
    session.permanent = True


@auth.route("/login", methods=["POST", "OPTIONS", "GET"])
@cross_origin()
def login_route():
    # check if user is already authenticated

    if request.method == "POST":
        # get username and password from form
        email: LiteralString = request.form["email"]
        password: LiteralString = request.form["password"]
        # query user with username
        user = User.query.filter_by(email=email).first()
        # check if user exists
        if user:
            # check if password is correct
            if user.check_password(password):
                try:
                    # login user
                    login_user(user, remember=True, force=True)
                    # make sure user is logged in
                    if user.is_authenticated:
                        print("User is authenticated")
                        return redirect(url_for("index_view.index_design"))
                except werkzeug.exceptions.HTTPException:
                    # if user is not authenticated
                    return render_template(
                        "login.html", error="Invalid username or password."
                    )
            else:
                # if password is not correct
                return render_template(
                    "login.html", error="Invalid username or password."
                )
        else:
            # if user does not exist
            return render_template("login.html", error="Invalid username or password.")
    else:
        # if request is not POST
        return render_template("login.html")


@auth.route("/register", methods=["POST", "GET"])
def register() -> Response or redirect or render_template or url_for or None:
    # docstring
    """Register a new user."""
    if request.method == "POST":
        # get username password and email from form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        # check if user exists
        if User.query.filter_by(username=username).first():
            # return error message
            return redirect(url_for("authentication.login"))
        else:
            # create user
            user = User(username=username, email=email, hashed_password=password)
            # add user to database
            db.session.add(user)
            # commit changes
            db.session.commit()
            # login user
            login_user(user)
            # redirect to home page
            return redirect(url_for("index_view.index_design"))
    else:
        # return register page
        return render_template("register.html")


@auth.route("/user", methods=["GET"])
@login_required
def user() -> Response or redirect or url_for or dict[str, Any] or None:
    # docstring
    """
    User page for the application.
    """
    if request.method == "GET":
        return (
            "this is the register route from the auth api <br><br><br> this is the address https://127.0.0.1:5000/register",
            300,
        )


@auth.route("/protected")
@flask_praetorian.auth_required
def protected():
    return jsonify(
        {
            "message": f"protected endpoint (allowed user {flask_praetorian.current_user().username})"
        }
    )


@auth.route("/get_user")
@flask_praetorian.auth_required
def user_query_route():
    return jsonify(
        {
            "id": f"{flask_praetorian.current_user().id})",
            "username": f"{flask_praetorian.current_user().username})",
            "email": f"{flask_praetorian.current_user().email})",
        }
    )


@auth.route("/logout")
@login_required
def logout() -> Response or redirect or url_for or None:
    # docstring
    """Logout the current user."""
    # logout user
    if request.method == "GET":
        logout_user()
    # redirect to home page
    return redirect(url_for("authentication.landing_page"))
