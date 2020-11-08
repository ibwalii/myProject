from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    image = db.Column(db.String(20), nullable = False, default = "default.jpg")
    posts = db.relationship('Post', backref='author', lazy = True)

    def __repr__(self):
        return f"Users('{self.username}','{self.email}, '{self.image}')"   

class Post (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    content = db.Column(db.String(200), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    userid = db.Column (db.Integer, db.ForeignKey('user.id'), nullable= False)

    def __repr__(self):
        return f"Posts ('{self.title}', '{self.date_posted})"