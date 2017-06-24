from flask import Blueprint

# initialize blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views
