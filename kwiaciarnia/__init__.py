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


UPLOAD_FOLDER_POSTS = 'kwiaciarnia/static/uploads/posts'
app.config['UPLOAD_FOLDER_POSTS'] = UPLOAD_FOLDER_POSTS
app.config['MAX_CONTENT_LENGHT'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


from kwiaciarnia import routes