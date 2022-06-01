from __future__ import annotations

from typing import *

import werkzeug
from flask import (Blueprint, Response, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from pyparsing import str_type
from typing_extensions import *

authentication_blueprint = Blueprint(
    "authentication",
    __name__,
    template_folder="templates",
)

from ..extension_globals.database import db
from .models import User


@authentication_blueprint.route("/")
@authentication_blueprint.route("/index", methods=["POST", "GET"])
def landing_page() -> Response or render_template:
    """
    Landing page for the application.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index_view.index_design"))
    # query all users
    return render_template("landing_page.html"), 200


@authentication_blueprint.route("/login", methods=["POST", "GET"])
def login() -> Response or redirect or render_template or url_for or None:
    # docstring
    """
    Login page for the application.
    """

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
                        return redirect(url_for("index_view.index_design")), 200
                except werkzeug.exceptions.HTTPException:
                    # if user is not authenticated
                    return (
                        render_template(
                            "login.html", error="Invalid username or password."
                        ),
                        302,
                    )
            else:
                # if password is not correct
                return (
                    render_template(
                        "login.html", error="Invalid username or password."
                    ),
                    302,
                )
        else:
            # if user does not exist
            return (
                render_template("login.html", error="Invalid username or password."),
                302,
            )
    else:
        # if request is not POST
        return render_template("login.html"), 200


@authentication_blueprint.route("/register", methods=["POST", "GET"])
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
            return redirect(url_for("authentication.login")), 302
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
            return redirect("/compression_service/"), 200
    else:
        # return register page
        return render_template("register.html"), 200


@authentication_blueprint.route("/user", methods=["GET"])
@login_required
def user() -> Response or redirect or url_for or dict[str, Any] or None:
    # docstring
    """
    User page for the application.
    """
    if request.method == "GET":
        # check if user is logged in
        try:
            if current_user.is_authenticated:
                # return user page
                return redirect(url_for("index_view.index_design"))
        except werkzeug.exceptions.HTTPException:
            # if user is not authenticated
            return redirect(url_for("authentication.login"))
        finally:
            # query user
            current_user_dict: dict[str, Any] = {
                "username": current_user.username,
                "email": current_user.email,
                "password": current_user.hashed_password,
            }
            return current_user_dict
    else:
        # if request is not GET
        return redirect(url_for("authentication.login"))


@authentication_blueprint.route("/logout")
@login_required
def logout() -> Response or redirect or url_for or None:
    # docstring
    """Logout the current user."""
    # logout user
    if request.method == "GET":
        logout_user()
    # redirect to home page
    return redirect(url_for("authentication.landing_page"))
