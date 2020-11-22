import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            NewPostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template('home.html', posts= posts)

@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author = user)\
            .order_by(Post.date_posted.desc())\
            .paginate(per_page=3, page=page)
    return render_template('user_post.html', posts= posts, user=user, page=1)

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

# save photo function
def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics/' , picture_fn)
    
    resized_image = Image.open(form_picture)
    resized_image.thumbnail((200,200))

    resized_image.save(picture_path)

    return picture_fn


@app.route('/account', methods = ['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_url = url_for('static', filename = 'profile_pics/'+ current_user.image)
    return render_template('account.html', title = 'Account', image_url = image_url, form = form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/newpost', methods = ['GET', 'POST'])
@login_required
def newPost():
    form = NewPostForm()
    if form.validate_on_submit():
        post1 = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post1)
        db.session.commit()
        flash('Post Added', category='success')
        return redirect(url_for('newPost'))
    return render_template('newpost.html', title = 'New Post', form = form)

@app.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def Blogpost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title , post=post )

@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def Update_Blogpost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post Updated', category='success')
        return redirect(url_for('Blogpost', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newpost.html', title = 'Update Post', form = form)

@app.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def Delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', category='success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token = User.get_reset_token(user)
    msg = Message('Password Reset', sender='techvalley2015@gmail.com', recipients=[user.email])
    msg.body = f''' Click Here to reset your password
        {url_for('reset_token', token = token, _external = True)}

        if you did not, ignore
    '''

@app.route('/reset_password', methods = ['GET', 'POST'])
def RequestResetPassword():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f'Reset has been sent to {form.email.data}', category='info')
    return render_template('reset_request.html', title='Reset password', form = form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid/Expired request', category='warning')
        return redirect(url_for('reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password_hash
        db.session.commit()
        flash(f'New password set', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form = form)