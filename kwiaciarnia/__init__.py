from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kwiaciarnia.db'
app.config['SECRET_KEY'] = '?D(G+KbPeShVmYq3'

db = SQLAlchemy(app)


from kwiaciarnia import routes