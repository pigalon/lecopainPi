from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from lecopain.extensions import db, ma, login_manager
import locale
from flask_ipban import IpBan

def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)


app = Flask(__name__)
ban_count = 20
ban_seconds = 2000
try:
    ip_ban = IpBan(app=app, ban_count=ban_count, ban_seconds=ban_seconds, record_dir='/tmp', persist=False)
    ip_ban.whitelist_add('127.0.0.1')
    ip_ban.whitelist_add('176.155.187.146')

except:
    pass

import logging, logging.config, yaml
logging.config.dictConfig(yaml.load(open('logging.conf'), Loader=yaml.FullLoader))

moment = Moment(app)
app.secret_key = 'super secret string'
app.config.from_object('config.BaseConfig')
register_extensions(app)

blueprint = Blueprint('main', __name__)
app.register_blueprint(blueprint)
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
