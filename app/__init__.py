import os
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
# from flask_script import Manager

app = Flask(__name__)
# database config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# admin config:
app.config['RE0BLOG_ADMIN'] = os.environ.get('RE0BLOG_ADMIN')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
    'hard to guess string'

# email config:
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['RE0BLOG_MAIL_SUBJECT_PREFIX'] = '[Re0-Blog]'
app.config['RE0BLOG_MAIL_SENDER'] = \
    f"Re0-Blog Admin <{app.config['MAIL_USERNAME']}>"
app.config['WTF_CSRF_ENABLED'] = False #!! test only
app.config['SERVER_NAME'] = '127.0.0.1:5000'

# ext init:
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
mail = Mail(app)
# manager = Manager(app)
from .api_1_0 import api as api_1_0_blueprint
app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

# Add context:
@app.context_processor
def inject_permissions():
    from app.models import Permission
    return dict(Permission=Permission)

# Add command:
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop: 
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

from app import views