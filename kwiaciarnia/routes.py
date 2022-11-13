from flask import render_template, redirect, url_for
from kwiaciarnia import app, db
from kwiaciarnia.forms import PostForm
from kwiaciarnia.models import Posts
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

@app.errorhandler(404)
def invalid_route(e):
    return 'Wprowadszono niepoprawny adres'

