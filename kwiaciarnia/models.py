from flask_login import UserMixin
from kwiaciarnia import db, login_manager
import datetime



class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=128))
    body = db.Column(db.Text())
    added = db.Column(db.DateTime(), default=datetime.datetime.now())
    likes = db.Column(db.Integer(), default=0)
    dislikes = db.Column(db.Integer(), default=0)
    def __repr__(self):
        return self.body()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=64), nullable= False, unique=True)
    email = db.Column(db.String(), nullable= False, unique=True)
    password_hash = db.Column(db.String(length=16), nullable= False)
    def __repr__(self):
        return self.username()


class Post_likes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_like = db.Column(db.Integer(), db.ForeignKey('user.id'))
    post_like = db.Column(db.Integer(), db.ForeignKey('posts.id'))

class Post_dislikes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_dislike = db.Column(db.Integer(), db.ForeignKey('user.id'))
    post_dislike = db.Column(db.Integer(), db.ForeignKey('posts.id'))