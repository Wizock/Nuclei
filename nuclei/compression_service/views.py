from flask import Blueprint, Flask

compression_service_blueprint = Blueprint("compression_service", __name__)

@compression_service_blueprint.route("/index")
def index():
    return "Hello, world!"

