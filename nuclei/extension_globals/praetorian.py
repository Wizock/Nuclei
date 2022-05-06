import flask_praetorian
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

guard: flask_praetorian = flask_praetorian.Praetorian()