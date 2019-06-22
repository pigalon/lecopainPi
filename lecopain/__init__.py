from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy


app                                   = Flask(__name__)
app.config['SECRET_KEY']              = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/site.db'
db                                    = SQLAlchemy(app)

main                                  = Blueprint('main', __name__)


from lecopain import routes 
from lecopain.dao import models
