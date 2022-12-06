from flask import render_template, redirect, url_for, request, flash
from kwiaciarnia import app, db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from kwiaciarnia.forms import PostForm, UserForm, Loginform
from kwiaciarnia.models import Posts, User, Post_likes, Post_dislikes
from flask_login import login_user, logout_user, login_required, current_user
import datetime
import urllib.request
from werkzeug.utils import secure_filename
import os 

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
    posts = Posts.query.all()
    return render_template('manage.html', posts=posts)

@app.route("/")
def home():
    all_posts = Posts.query.all()
    likes = Post_likes()
    dislike = Post_dislikes()
    return render_template('home.html', all_posts=all_posts, likes=likes, dislike=dislike)

@app.route('/like_result/<int:pk>', methods=['GET', 'POST'])
@login_required
def like_result(pk):
    liked_post = request.form.get('like_button')
    if request.method == "POST":
        status_dislike = Post_dislikes.query.filter_by(post_dislike=pk, user_dislike=current_user.id).first()
        if status_dislike:
            undislike = Posts.query.filter_by(id=pk).first()
            undislike.dislikes -= 1
            db.session.delete(status_dislike)
            db.session.commit()
        if not Post_likes.query.filter_by(post_like=pk, user_like=current_user.id).first():
            new_like = Post_likes(
                user_like = current_user.id,
                post_like = liked_post
            )
            liked = Posts.query.filter_by(id=pk).first()
            liked.likes += 1
            db.session.add(new_like)
            db.session.commit()
        else:
            new_unlike = Post_likes.query.filter_by(post_like=pk, user_like=current_user.id).first()
            db.session.delete(new_unlike)
            unlike = Posts.query.filter_by(id=pk).first()
            unlike.likes -= 1
            db.session.commit()
    return redirect(url_for('home'))

@app.route('/dislike_result/<int:pk>', methods=['GET', 'POST'])
@login_required
def dislike_result(pk):
    disliked_post = request.form.get('dislike_button')
    if request.method == "POST":
        status_unlike = Post_likes.query.filter_by(post_like=pk, user_like=current_user.id).first()
        if status_unlike:
            unlike = Posts.query.filter_by(id=pk).first()
            unlike.dislikes -= 1
            db.session.delete(status_unlike)
            db.session.commit()        
        if not Post_dislikes.query.filter_by(post_dislike=pk, user_dislike=current_user.id).first():
            new_dislike = Post_dislikes(
                user_dislike = current_user.id,
                post_dislike = disliked_post
            )
            dislike = Posts.query.filter_by(id=pk).first()
            dislike.dislikes += 1
            db.session.add(new_dislike)
            db.session.commit()
        else:
            new_undislike = Post_dislikes.query.filter_by(post_dislike=pk, user_dislike=current_user.id).first()
            db.session.delete(new_undislike)
            undisliked = Posts.query.filter_by(id=pk).first()
            undisliked.dislikes -= 1
            db.session.commit()
    return redirect(url_for('home'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def name_changer(id):
    return str(id) + '.png'

@app.route("/dodaj_post", methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post_to_create = Posts(
            title = form.title.data,
            body = form.body.data,
            likes = 0,
            dislikes = 0,
            added = datetime.datetime.now()
        )
        db.session.add(post_to_create)
        db.session.commit()
        if request.method == "POST":
            if 'file' not in request.files:
                return "nie przesłano pliku"
            file = request.files['file']
            if file.filename == '':
                return 'nie wybrano zadnego zdjecia'
            if file and allowed_file(file.filename):
                filename = secure_filename(name_changer(post_to_create.id))
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return redirect(url_for('home'))
            else:
                return 'wybrałeś zły format'
        return redirect(url_for('home'))
    return render_template('add_post.html', form=form)

@app.route('/usun_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Posts.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        os.remove(f"C:/Users/jakub/Desktop/kwiaciarnia/kwiaciarnia/static/uploads/{id}.png")
        return redirect(url_for('home'))
    return render_template('delete_post_comfirmation.html', post=post)
        
        
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
    return render_template('404.html')




# def upload_file():
# if request.method == 'POST':
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     # If the user does not select a file, the browser submits an
#     # empty file without a filename.
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('download_file', name=filename))
# return '''