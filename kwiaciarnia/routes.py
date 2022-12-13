from flask import render_template, redirect, url_for, request, flash
from kwiaciarnia import app, db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_POSTS, UPLOAD_FOLDER_PRODUCTS
from kwiaciarnia.forms import PostForm, UserForm, Loginform, AddProductForm, OrderForm
from kwiaciarnia.models import Posts, User, Post_likes, Post_dislikes, Products, Product_category, Orders
from flask_login import login_user, logout_user, login_required, current_user
import datetime
import urllib.request                                                                               #without that u r unable to create/edit db
from werkzeug.utils import secure_filename
import os 

#   oK5XKfRTkmBZShUafzZF
@app.route('/oK5XKfRTkmBZShUafzZF')
def stworz():
    db.create_all()
    return "baza danych stworzona"

# #   BZDbQm7C2thGaocmuCWJ
# @app.route('/BZDbQm7C2thGaocmuCWJ')
# def admin():
#     new_admin = User.query.filter_by(id=current_user.id).first()
#     if new_admin:
#         new_admin.is_admin = True
#         new_admin.is_stuff = True
#         db.session.commit()
#         return 'ok'
#     return "witaj nowy admine"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def name_changer(id):
    return str(id) + '.png'
def add_photo(id, folder_name):
    if request.method == "POST":
        if 'file' not in request.files:
            print("nie przesłano pliku")
        file = request.files['file']
        if file.filename == '':
            print('nie wybrano zadnego zdjecia')
        if file and allowed_file(file.filename):
            filename = secure_filename(name_changer(id))
            file.save(os.path.join(app.config[f"{folder_name}"], filename))
            return redirect(url_for('home'))
        else:
            print('wybrałeś zły format')

@app.route("/")
def home():
    all_posts = Posts.query.order_by(Posts.id.desc())
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
        add_photo(post_to_create.id, 'UPLOAD_FOLDER_POSTS')
        return redirect(url_for('home'))
    return render_template('add_post.html', form=form)

@app.route('/usun_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Posts.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        os.remove(f"C:/Users/jakub/Desktop/kwiaciarnia/kwiaciarnia/static/uploads/posts/{id}.png")
        return redirect(url_for('home'))
    return render_template('delete/delete_post_comfirmation.html', post=post)
 
@app.route('/oferta')
def products_categories():
    products_to_sale_category = Product_category.query.group_by(Product_category.name).all()
    products_to_sale_id = Products.query.group_by(Products.category).all()
    return render_template('products_categories.html', products_to_sale_category=products_to_sale_category, products_to_sale_id=products_to_sale_id)

@app.route('/oferta/<cat_name>/<id>', methods=["GET", "POST"])
def products(cat_name, id):
    products = Products.query.filter_by(category=id).all()
    products_category = Product_category.query.filter_by(name=cat_name).first()
    form = OrderForm()
    if request.method == "POST":
        new_order = Orders(
            phone_number = request.form["phone-number"],
            product = request.form["product"]
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('products.html', products=products, products_category=products_category, form=form)

def check_if_category_exist(name):
    if Product_category.query.filter_by(name=name).first() is not None:
        category_id = Product_category.query.filter_by(name=name).first()
        return category_id.id
    else:
        category_id = Product_category(
            name = name
        )
        db.session.add(category_id)
        db.session.commit()
        return category_id.id

@app.route('/dodaj produkt', methods=["GET", "POST"])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        new_product = Products(
            category = check_if_category_exist(form.category.data),
            name = form.name.data,
            description = form.description.data,
            price = form.price.data,
        )
        db.session.add(new_product)
        db.session.commit()
        add_photo(new_product.id, 'UPLOAD_FOLDER_PRODUCTS')
        return redirect(url_for('home'))
    print(form.validate_on_submit())
    return render_template('add_product.html', form=form)

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

@app.route('/zarządzaj')
def manage():
    return render_template('manage/manage.html')

@app.route("/zarządzaj/posty")
def manage_posts():
    posts = Posts.query.order_by(Posts.id.desc())
    return render_template('manage/manage_posts.html', posts=posts)

@app.route("/zarządzaj/produkty")
def manage_products():
    products = Products.query.order_by(Products.id.desc())
    return render_template('manage/manage_products.html', products=products)

@app.route('/usun_produkt/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    product = Products.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        os.remove(f"C:/Users/jakub/Desktop/kwiaciarnia/kwiaciarnia/static/uploads/products/{id}.png")
        return redirect(url_for('home'))
    return render_template('delete/delete_post_comfirmation.html', product=product)
 