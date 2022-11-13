from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from kwiaciarnia.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kwiaciarnia.db'
app.config['SECRET_KEY'] = '?D(G+KbPeShVmYq3'

db.init_app(app)


from kwiaciarnia import routes