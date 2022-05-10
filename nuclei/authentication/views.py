import base64, datetime, hashlib, os, pathlib
from typing import Any, final


from flask import (Blueprint, Response, redirect, render_template, request, 
                   url_for)
from flask_login import login_required, login_user, logout_user, current_user
import werkzeug

authentication_blueprint = Blueprint(
    "authentication",
    __name__,
    template_folder="templates",
)

from ..extension_globals.database import db
from .models import User


@authentication_blueprint.route("/")
@authentication_blueprint.route("/index", methods=["POST", "GET"])
def landing_page():
    """
    Landing page for the application.
    """
    # query all users
    return render_template("landing_page.html")


@authentication_blueprint.route("/login", methods=["POST", "GET"])
def login():
    # docstring
    """
    Login page for the application.
    """

    if request.method == "POST":
        # get username and password from form
        email = request.form["email"]
        password = request.form["password"]
        # query user with username
        user = User.query.filter_by(email=email).first()
        # check if user exists
        if user:
            # check if password is correct
            if user.check_password(password):
                try:
                    # login user
                    login_user(user, remember=True, force=True, fresh=True)
                    # make sure user is logged in
                    if user.is_authenticated:
                        print("User is authenticated")
                        return redirect(url_for("compression_service.index_design"))
                except werkzeug.exceptions.HTTPException:
                    # if user is not authenticated
                    return render_template("login.html", error="Invalid username or password.")
            else:
                # if password is not correct
                return render_template("login.html", error="Invalid username or password.")
        else:
            # if user does not exist
            return render_template("login.html", error="Invalid username or password.")
    else:
        # if request is not POST
        return render_template("login.html")

@authentication_blueprint.route("/register", methods=["POST", "GET"])
def register():
    # docstring
    """Register a new user."""
    if request.method == "POST":
        # get username password and email from form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        print(username, password, email)
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
            return redirect('/compression_service/')
    else:
        # return register page
        return render_template("register.html")

@authentication_blueprint.route("/user")
def user():
    # docstring
    """
    User page for the application.
    """
    # query user
    current_user_dict:dict[str, Any] = {
        "username": current_user.username,
        "email": current_user.email,
        "password": current_user.hashed_password,
    }
    # return user page
    return render_template("user.html", current_user= current_user_dict)

@authentication_blueprint.route("/logout")
@login_required
def logout():
    # docstring
    """Logout the current user."""
    # logout user
    logout_user()
    # redirect to home page
    return redirect(url_for("authentication.landing_page"))
