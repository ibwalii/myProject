from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import NewPostForm

posts = Blueprint('posts', __name__)


@posts.route('/newpost', methods = ['GET', 'POST'])
@login_required
def newPost():
    form = NewPostForm()
    if form.validate_on_submit():
        post1 = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post1)
        db.session.commit()
        flash('Post Added', category='success')
        return redirect(url_for('posts.newPost'))
    return render_template('newpost.html', title = 'New Post', form = form)

@posts.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def Blogpost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title , post=post )

@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
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
        return redirect(url_for('posts.Blogpost', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newpost.html', title = 'Update Post', form = form)

@posts.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def Delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', category='success')
    return redirect(url_for('main.home'))