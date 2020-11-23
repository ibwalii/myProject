from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog import db, bcrypt
from flaskblog.models import Post, User
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

users = Blueprint('users', __name__, )


@users.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_url = request.args.get('next')
            if next_url:
                next_url = next_url.replace('/', '')
            return redirect(url_for(next_url)) if next_url else redirect(url_for('main.home'))
        else:
            flash(f'Username: {form.email.data} or password incorrect', 'danger')
    return render_template('login.html', title='Login Page', form = form) 

@users.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password = password_hash, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Registration', form = form)


@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_url = save_photo(form.image_file.data)
            current_user.image = image_url
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Account Updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_url = url_for('static', filename = 'profile_pics/'+ current_user.image)
    return render_template('account.html', title = 'Account', image_url = image_url, form = form)

@users.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author = user)\
            .order_by(Post.date_posted.desc())\
            .paginate(per_page=3, page=page)
    return render_template('user_post.html', posts= posts, user=user, page=1)

@users.route('/reset_password', methods = ['GET', 'POST'])
def RequestResetPassword():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f'Reset has been sent to {user.email}', category='info')
    return render_template('reset_request.html', title='Reset password', form = form)

@users.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid/Expired request', category='warning')
        return redirect(url_for('users.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password_hash
        db.session.commit()
        flash(f'New password set', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form = form)