from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id =  s.loads(token)['user_id']
        except:
            return None
        return User.query.get(int(user_id))

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