from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app                                   = Flask(__name__)
app.secret_key = 'super secret string'


app.config['SECRET_KEY']              = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/site.db'
db                                    = SQLAlchemy(app)

main                                  = Blueprint('main', __name__)

login_manager 						  = LoginManager(app)
#login_manager.init_app(app)
login_manager.login_view = 'home'



from lecopain import routes
from lecopain.dao import models
