import flask_praetorian
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

guard: flask_praetorian = flask_praetorian.Praetorian()
