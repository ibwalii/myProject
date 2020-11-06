from flask import render_template, flash, redirect, url_for
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'ibwalii@wali.com' and form.password.data == 'pass':
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Username: {form.email.data} or password incorrect', 'danger')
    return render_template('login.html', title='Login Page', form = form) 

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration', form = form)

