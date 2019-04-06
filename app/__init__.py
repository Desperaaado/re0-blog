import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASKY_ADMIN'] = 'xiao0yu0xiang0@qq.com' #!! from $env
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'hard to guess string'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)

from app import views