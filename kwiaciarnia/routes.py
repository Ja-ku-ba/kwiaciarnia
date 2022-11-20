from flask import render_template, redirect, url_for, request
from kwiaciarnia import app, db
from kwiaciarnia.forms import PostForm, UserForm, Loginform
from kwiaciarnia.models import Posts, User
from flask_login import login_user, logout_user, login_required, current_user
import datetime
# oK5XKfRTkmBZShUafzZF
@app.route('/oK5XKfRTkmBZShUafzZF')
def stworz():
    db.create_all()
    return "weszło"

@app.route("/")
def home():
    all_posts = Posts.query.all()
    return render_template('index.html', all_posts=all_posts)

@app.route('/like_result', methods=['GET', 'POST'])
def like_result():
    if request.method == "POST":
        return 'cudo'
    return "zaskoczyło"

@app.route("/dodaj_post", methods=['GET', 'POST'])
def add_post():
    add_post = PostForm()
    if add_post.validate_on_submit():
        post_to_create = Posts(
            title = add_post.title.data,
            body = add_post.body.data,
            likes = 0,
            dislikes = 0,
            added = datetime.datetime.now()
        )
        db.session.add(post_to_create)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_post.html', add_post=add_post)

@app.route('/kotakt')
def contact():
    return render_template('contact.html')

@app.route('/zarejestruj', methods=['GET', 'POST'])
def register():
    form  = UserForm()
    if form.validate_on_submit():
        new_user = User(
            username = form.username.data, 
            password_hash = form.password1.data,
            email = form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route("/zaloguj", methods=["GET", "POST"])
def login():
    form = Loginform()
    if request.method == "POST":
        user_to_login = User.query.filter_by(email=form.email.data).first()
        login_user(user_to_login)
        return redirect(url_for("home"))
    return render_template('login.html', form=form)

@app.route("/wuloguj")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.errorhandler(404)
def invalid_route(e):
    return 'Wprowadszono niepoprawny adres'

