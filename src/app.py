# src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt  # add this new line


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    # initializing bcrypt
    bcrypt.init_app(app)  # add this line

    db.init_app(app)  # add this line

    #####################
    # existing code remain #
    ######################

    return app