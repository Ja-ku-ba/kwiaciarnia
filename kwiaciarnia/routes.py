from flask import render_template, redirect, url_for, request, flash
from kwiaciarnia import app, db
from kwiaciarnia.forms import PostForm, UserForm, Loginform
from kwiaciarnia.models import Posts, User, Post_likes, Post_dislikes
from flask_login import login_user, logout_user, login_required, current_user
import datetime
#   oK5XKfRTkmBZShUafzZF
@app.route('/oK5XKfRTkmBZShUafzZF')
def stworz():
    db.create_all()
    return "baza danych stworzona"

#   BZDbQm7C2thGaocmuCWJ
@app.route('/BZDbQm7C2thGaocmuCWJ')
def admin():
    new_admin = User.query.filter_by(id=current_user.id).first()
    if new_admin:
        new_admin.is_admin = True
        new_admin.is_stuff = True
        db.session.commit()
        return 'ok'
    return "witaj nowy admine"

@app.route('/manage')
def manage():
    return render_template('manage.html')

@app.route("/")
def home():
    all_posts = Posts.query.all()
    likes = Post_likes()
    dislike = Post_dislikes()
    return render_template('index.html', all_posts=all_posts, likes=likes, dislike=dislike)

@app.route('/like_result', methods=['GET', 'POST'])
@login_required
def like_result():
    liked_post = request.form.get('like_button')
    if request.method == "POST":
        if Post_dislikes.query.filter_by(user_dislike=current_user.id).first():
            new_undislike = Post_dislikes.query.filter_by(user_dislike=current_user.id).first()
            new_undislike.user_dislike = None
            new_undislike.post_dislike = None
            db.session.commit()
        if not Post_likes.query.filter_by(user_like=current_user.id).first():
            new_like = Post_likes(
                user_like = current_user.id,
                post_like = liked_post
            )
            db.session.add(new_like)
            db.session.commit()
        else:
            new_unlike = Post_likes.query.filter_by(user_like=current_user.id).first()
            new_unlike.user_like = None
            new_unlike.post_like = None
            db.session.commit()
    return redirect(url_for('home'))

@app.route('/dislike_result', methods=['GET', 'POST'])
@login_required
def dislike_result():
    disliked_post = request.form.get('dislike_button')
    if request.method == "POST":
        if Post_likes.query.filter_by(user_like=current_user.id).first():
            new_unlike = Post_likes.query.filter_by(user_like=current_user.id).first()
            new_unlike.user_like = None
            new_unlike.post_like = None
            db.session.commit()
        if not Post_dislikes.query.filter_by(user_dislike=current_user.id).first():
            new_dislike = Post_dislikes(
                user_dislike = current_user.id,
                post_dislike = disliked_post
            )
            db.session.add(new_dislike)
            db.session.commit()
        else:
            new_undislike = Post_dislikes.query.filter_by(user_dislike=current_user.id).first()
            new_undislike.user_dislike = None
            new_undislike.post_dislike = None
            db.session.commit()
    return redirect(url_for('home'))

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
            password = form.password1.data,
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
    if form.validate_on_submit():
        user_to_login = User.query.filter_by(email=form.email.data).first()
        if user_to_login and user_to_login.check_password_correction(attempted_password=form.password.data):
            print('imo')
            login_user(user_to_login)
            return redirect(url_for("home"))
        else:
            flash('Wprowadzony emial, lub hasło jest błędne', category='danger')
    return render_template('login.html', form=form)

@app.route("/wuloguj")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.errorhandler(404)
def invalid_route(e):
    return 'Wprowadszono niepoprawny adres'
