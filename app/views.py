from flask import render_template, url_for, flash, redirect, request
from flask_login import (login_user, 
    logout_user, current_user, login_required)
from app import app, db
from app.models import User, Permission, Post
from app.forms import RegistrationForm, LoginForm, PostForm
from app.email import send_email

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)

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
        login_user(user) # Automatic login after registration
        token = user.generate_confirmation_token()
        send_email(user.email, 
                   'Confirm Your Account',
                   'auth/email/confirm', 
                   user=user, 
                   token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
        
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index'))