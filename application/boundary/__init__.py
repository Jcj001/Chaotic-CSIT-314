from flask import Blueprint
from .authentication import authentication
from .system_admin import admin
from .cafe_owner import owner

boundary = Blueprint('boundary', __name__, template_folder="templates", static_folder="assets")

# BLUEPRINTS REGISTRATION
boundary.register_blueprint(authentication)
boundary.register_blueprint(admin)
boundary.register_blueprint(owner)
