from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'ibrahim bakari',
        'title': 'test 1',
        'content': 'testing content 1',
        'date_posted': 'Nov 5, 2020'
    },
    {
        'author': 'ibrahim bakari',
        'title': 'test 1',
        'content': 'testing content 1',
        'date_posted': 'Nov 5, 2020'
    }

]


@app.route('/')
def home():
    return render_template('home.html', posts= posts)

@app.route('/about')
def about():
    return render_template('about.html', title='about us')

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_url = request.args.get('next')
            if next_url:
                next_url = next_url.replace('/', '')
            return redirect(url_for(next_url)) if next_url else redirect(url_for('home'))
        else:
            flash(f'Username: {form.email.data} or password incorrect', 'danger')
    return render_template('login.html', title='Login Page', form = form) 

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password = password_hash, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form = form)

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title = 'Account')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

