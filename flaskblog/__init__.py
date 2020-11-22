from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import  Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

app.config ['SECRET_KEY'] = 'f1b4c8ba43d3e1c31004b7055e368fbc'
app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config ['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config ['MAIL_PORT'] = 587
app.config ['MAIL_USE_TSL'] = True
app.config ['MAIL_USERNAME'] = 'techvalley2015@gmail.com'
app.config ['MAIL_PASSWORD'] = 'Techvalley@2015'
mail = Mail(app)

from flaskblog import routes