from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user
from app import app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user() 
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Login success.')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
