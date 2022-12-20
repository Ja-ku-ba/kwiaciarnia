from flask_login import UserMixin
from kwiaciarnia import db, login_manager, bcrypt
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=64), nullable= False, unique=True)
    email = db.Column(db.String(), nullable= False, unique=True)
    password_hash = db.Column(db.String(length=16), nullable= False)
    is_admin = db.Column(db.Boolean(), default=False)
    def __repr__(self):
        return self.username()

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('UTF-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    body = db.Column(db.Text())
    added = db.Column(db.DateTime(), default=datetime.datetime.now())
    likes = db.Column(db.Integer(), default=0)
    dislikes = db.Column(db.Integer(), default=0)
    def __repr__(self):
        return self.id()

class Post_likes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_like = db.Column(db.Integer(), db.ForeignKey('user.id'))
    post_like = db.Column(db.Integer(), db.ForeignKey('posts.id'))

class Post_dislikes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_dislike = db.Column(db.Integer(), db.ForeignKey('user.id'))
    post_dislike = db.Column(db.Integer(), db.ForeignKey('posts.id'))

class Product_category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30))

class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.Integer(), db.ForeignKey('product_category.id'))
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())
    price = db.Column(db.Integer())

class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product = db.Column(db.Integer(), db.ForeignKey('products.id'))
    phone_number = db.Column(db.String())
    buyer = db.Column(db.Integer(), db.ForeignKey('user.id'))
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.phone_number()

class SocialMedia(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    social_media_link = db.Column(db.String())
    madia = db.Column(db.String())

class Contact(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    phone_number = db.Column(db.Integer())
    number_owner = db.Column(db.String())
    
class Adres(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    addres = db.Column(db.String())