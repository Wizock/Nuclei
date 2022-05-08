import base64
import datetime
import hashlib
import os
import pathlib

from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

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
    # query all users
    return render_template("landing_page.html")


@authentication_blueprint.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # get username and password from form
        username = request.form["username"]
        password = request.form["password"]
        # query user with username
        user = User.query.filter_by(username=username).first()
        # check if user exists
        if user:
            # check if password is correct
            if user.check_password(password):
                # login user
                login_user(user)
                # redirect to home page
                return redirect(url_for("compression_service.index"))
            else:
                # return error message
                return render_template("login.html", error="Incorrect password")
        else:
            # return error message
            return render_template("login.html", error="User does not exist")
    else:
        # return login page
        return render_template("login.html")


@authentication_blueprint.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # get username password and email from form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        print(username, password, email)
        # check if user exists
        if User.query.filter_by(username=username).first():
            # return error message
            return render_template("register.html", error="User already exists")
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
            return redirect(url_for("compression_service.index_design"))
    else:
        # return register page
        return render_template("register.html")


@authentication_blueprint.route("/logout")
@login_required
def logout():
    # logout user
    logout_user()
    # redirect to home page
    return redirect(url_for("authentication.landing_page"))
