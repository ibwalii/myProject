from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config ['SECRET_KEY'] = 'f1b4c8ba43d3e1c31004b7055e368fbc'
app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
db = SQLAlchemy(app)

from flaskblog import routes