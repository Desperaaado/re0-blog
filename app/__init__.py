from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['FLASKY_ADMIN'] = 'xiao0yu0xiang0@qq.com' #!! from $env
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import views