from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text())
    added = db.Column(db.DateTime(), default=datetime.datetime.now())
    likes = db.Column(db.Integer(), default=0)
    dislikes = db.Column(db.Integer(), default=0)
    def __repr__(self):
        return self.body()
