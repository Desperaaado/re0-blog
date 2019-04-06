from flask import render_template, url_for, flash, redirect
from app import app, db
from app.models import User
from app.forms import RegistrationForm

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('index')) #!! >>login
    return render_template('register.html', form=form)
