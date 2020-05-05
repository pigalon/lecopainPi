from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restplus import Api
from lecopain.extensions import db, login_manager


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


app = Flask(__name__)
app.secret_key = 'super secret string'
app.config.from_object('config.BaseConfig')
register_extensions(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/')
app.register_blueprint(blueprint)
