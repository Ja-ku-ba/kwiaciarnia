from flask import render_template, redirect, url_for, request, flash
from kwiaciarnia import app, db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_POSTS, UPLOAD_FOLDER_PRODUCTS
from kwiaciarnia.forms import PostForm, UserForm, Loginform, AddProductForm, BuyForm, SocialMediaForm, ContactForm, AdresForm
from kwiaciarnia.models import Posts, User, Post_likes, Post_dislikes, Products, Product_category, Orders, Contact, SocialMedia, Adres
from flask_login import login_user, logout_user, login_required, current_user
import datetime
import urllib.request                                                                               #without that u r unable to create/edit db
from werkzeug.utils import secure_filename
import os 

# #   oK5XKfRTkmBZShUafzZF                                                                            #updating db
# @app.route('/oK5XKfRTkmBZShUafzZF')
# def stworz():
#     db.create_all()
#     return "db updated"


# #   BZDbQm7C2thGaocmuCWJ                                                                          #adding new admin
# @app.route('/BZDbQm7C2thGaocmuCWJ')
# def admin():
#     new_admin = User.query.filter_by(id=current_user.id).first()
#     if new_admin:
#         new_admin.is_admin = True
#         new_admin.is_stuff = True
#         db.session.commit()
#         return 'ok'
#     return "Hello to new admin"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def name_changer(id):
    return str(id) + '.png'
def add_photo(id, folder_name):
    if request.method == "POST":
        if 'file' not in request.files:
            flash(f'Nie przesłano pliku', category='warning')
        file = request.files['file']
        if file.filename == '':
            flash(f'Nie wybrano zadnego zdjecia', category='warning')
        if file and allowed_file(file.filename):
            filename = secure_filename(name_changer(id))
            file.save(os.path.join(app.config[f"{folder_name}"], filename))
            return redirect(url_for('home'))
        else:
            flash(f'Wybrałeś zły format', category='warning')


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
        #checks if user already dislikes this post
        if status_dislike:
            db.session.delete(status_dislike)
            db.session.commit()
            undislike = Posts.query.filter_by(id=pk).first()
            undislike.dislikes = Post_dislikes.query.filter_by(post_dislike=pk).count()
            db.session.commit()
        #adds like if user already dont likes this post yet
        if not Post_likes.query.filter_by(post_like=pk, user_like=current_user.id).first():
            new_like = Post_likes(
                user_like = current_user.id,
                post_like = liked_post
            )
            db.session.add(new_like)
            db.session.commit()
            liked = Posts.query.filter_by(id=pk).first()
            liked.likes = Post_likes.query.filter_by(post_like=pk).count()
            db.session.commit()
        #unlike post if user already likes it
        else:
            new_unlike = Post_likes.query.filter_by(post_like=pk, user_like=current_user.id).first()
            db.session.delete(new_unlike)
            db.session.commit()
            unlike = Posts.query.filter_by(id=pk).first()
            unlike.likes = Post_likes.query.filter_by(post_like=pk).count()
            db.session.commit()
    return redirect(url_for('home'))


@app.route('/dislike_result/<int:pk>', methods=['GET', 'POST'])
@login_required
def dislike_result(pk):
    disliked_post = request.form.get('dislike_button')
    if request.method == "POST":
        status_unlike = Post_likes.query.filter_by(post_like=pk, user_like=current_user.id).first()
        #checks if user already likes this post
        if status_unlike:
            db.session.delete(status_unlike)
            db.session.commit()     
            unlike = Posts.query.filter_by(id=pk).first()
            unlike.dislikes = Post_likes.query.filter_by(post_like=pk).count()
            db.session.commit()     
        #adds like if user already dont dislikes this post yet
        if not Post_dislikes.query.filter_by(post_dislike=pk, user_dislike=current_user.id).first():
            new_dislike = Post_dislikes(
                user_dislike = current_user.id,
                post_dislike = disliked_post
            )
            db.session.add(new_dislike)
            db.session.commit()
            dislike = Posts.query.filter_by(id=pk).first()
            dislike.dislikes = Post_dislikes.query.filter_by(post_dislike=pk).count()
            db.session.commit()
        #undislike post if user already dislikes it
        else:
            new_undislike = Post_dislikes.query.filter_by(post_dislike=pk, user_dislike=current_user.id).first()
            db.session.delete(new_undislike)
            db.session.commit()
            undisliked = Posts.query.filter_by(id=pk).first()
            undisliked.dislikes = Post_dislikes.query.filter_by(post_dislike=pk).count()
            db.session.commit()
    return redirect(url_for('home'))


@app.route("/dodaj_post", methods=['GET', 'POST'])
@login_required
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
        flash('Post został pomyślnie dodany', category='success')
        return redirect(url_for('home'))
    return render_template('manage/manage_add_post.html', form=form)
 

@app.route('/oferta')
def products_categories():
    products_to_sale_category = Product_category.query.group_by(Product_category.name).all()
    products_to_sale_id = Products.query.group_by(Products.category).all()
    return render_template('products_categories.html', products_to_sale_category=products_to_sale_category, products_to_sale_id=products_to_sale_id)


@app.route('/oferta/<cat_name>/<id>', methods=["GET", "POST"])
def products(cat_name, id):
    products = Products.query.filter_by(category=id).all()
    products_category = Product_category.query.filter_by(name=cat_name).first()
    form = BuyForm()
    if form.validate_on_submit():
        order_time = datetime.datetime.now()
        ord_time = f"{order_time.strftime('%d')}/{order_time.strftime('%m')}/{order_time.strftime('%y')} {order_time.strftime('%X')}"
        new_order = Orders(
            phone_number = form.phone_number.data,
            product = request.form["product_id"],
            buyer = current_user.id,
            time = ord_time
        )
        db.session.add(new_order)
        db.session.commit()
        flash('Oczekuj na połączenie od naszego pracownika', category='success')
        return redirect(url_for("products", cat_name=cat_name, id=id))
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
        flash('Proodukt został pomyślnie dodany', category='success')
        products_category = Product_category.query.filter_by(id=new_product.category).first()
        return redirect(url_for("products", cat_name=products_category.name, id=products_category.id))
    return render_template('manage/manage_add_product.html', form=form)


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
            flash(f'Zalogowano się pomyślnie', category='success')
            login_user(user_to_login)
            return redirect(url_for("home"))
        else:
            flash('Nazwa użytkownika lub hasło zostało wprowadzne niepoprawnie', category='danger')
    return render_template('login.html', form=form)


@app.route("/wuloguj")
@login_required
def logout():
    logout_user()
    flash('Wylogowano pomyślnie', category='info')
    return redirect(url_for("home"))


@app.route('/uzytkownik/<name>')
def user_page(name):
    user_id = User.query.filter_by(username = name).first()
    user_purchases = Orders.query.filter_by(buyer=user_id.id).order_by(Orders.id.desc()).all()
    products = Products.query.all()
    return render_template('user_page.html', user_purchases=user_purchases, user_id=user_id, products=products)


@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.route('/zarządzaj')
@login_required
def manage():
    return render_template('manage/manage.html')


@app.route("/zarządzaj/posty")
@login_required
def manage_posts():
    posts = Posts.query.order_by(Posts.id.desc())
    return render_template('manage/manage_posts.html', posts=posts)


@app.route('/usun_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Posts.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        try:
            flash('Post został pomyślnie usunięty', category='info')
            os.remove(f"C:/Users/jakub/Desktop/kwiaciarnia/kwiaciarnia/static/uploads/posts/{id}.png")
        except:
            return redirect(url_for('manage_posts'))
        return redirect(url_for('manage_posts'))
    return render_template('delete/delete_post_comfirmation.html', post=post)


@app.route("/zarządzaj/produkty")
@login_required
def manage_products():
    products = Products.query.order_by(Products.id.desc())
    return render_template('manage/manage_products.html', products=products)


@app.route('/usun_produkt/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    product = Products.query.filter_by(id=id).first()
    cat = Product_category.query.filter_by(id=product.category).first()
    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        delete_category = Products.query.filter_by(category=cat.id).first()
        if delete_category is None:
            db.session.delete(cat)
            db.session.commit()
        try:
            flash('Produkt został pomyślnie usunięty', category='info')
            os.remove(f"C:/Users/jakub/Desktop/kwiaciarnia/kwiaciarnia/static/uploads/products/{id}.png")
        except:
            return redirect(url_for('manage_products'))
        return redirect(url_for('manage_products'))
    return render_template('delete/delete_product_comfirmation.html', product=product)


@app.route('/zarządzaj/kategorie', methods=["GET", "POST"])
@login_required
def manage_categories():
    categories = Product_category.query.all()
    if request.method == "POST":
        try:
            if request.form["new-category-name"]:
                current_category = Product_category.query.filter_by(id=request.form["old-name-id"]).first()
                current_category.name = request.form["new-category-name"]
                db.session.commit() 
                flash('Nazwa kategorii została pomyślnie usunięta', category='info')
                return redirect(url_for("products_categories"))
        except:
            if request.form["delete-category"]:
                Products.query.filter_by(category=request.form["delete-category"]).delete()
                current_category = Product_category.query.filter_by(id=request.form["delete-category"]).first()
                db.session.delete(current_category)
                db.session.commit()
                flash('Kategoria i produkty do niej przypisane zostały pomyślnie usunięte', category='info')
                return redirect(url_for("products_categories"))
    return render_template('manage/manage_categories.html', categories=categories)


@app.route('/zarządzaj/kontakt', methods=["GET", "POST"])
def manage_contact():
    data_contact = Contact.query.all()
    contact_form = ContactForm()
    data_socials = SocialMedia.query.all()
    socials_form = SocialMediaForm()
    data_addres = Adres.query.all()
    addres_form = AdresForm()
    if request.method == "POST":
        if addres_form.validate_on_submit():
            new_addres = Adres(
                addres = addres_form.addres.data
            )
            flash('Adres został pomyślnie dodany', category='info')
            db.session.add(new_addres)
        elif contact_form.validate_on_submit():
            new_number = Contact(
                phone_number = contact_form.phone_number.data,
                number_owner = contact_form.number_owner.data
            )
            flash('Numer został pomyślnie dodany', category='info')
            db.session.add(new_number)
        elif socials_form.validate_on_submit():
            new_link = SocialMedia(
                social_media_link = socials_form.social_media_link.data,
                madia = socials_form.media.data
            )
            flash('Link został pomyślnie dodany', category='info')
            db.session.add(new_link)
        else:
            flash('Co poszło nie tak', category='danger')
        db.session.commit()
        return redirect(url_for("manage_contact"))
    return render_template('manage/manage_contact.html', data_contact=data_contact, data_socials=data_socials, data_addres=data_addres, contact_form=contact_form, socials_form=socials_form, addres_form=addres_form)


@app.route('/zarządzaj/zamówienia', methods=["GET", "POST"])
def manage_orders():
    orders_list = Orders.query.filter_by(status=False).order_by(Orders.id.desc()).all()
    if request.method == "POST":
        order = request.form["done"]
        order_product = Orders.query.filter_by(product=order).first()
        order_product.status = True
        db.session.commit()
        return redirect(url_for('manage_orders'))
    return render_template('manage/manage_orders.html', orders_list=orders_list, products=products)


@app.route('/zarządzaj/zamówienia/zrealizowane', methods=["GET", "POST"])
def manage_orders_done():
    orders_list_done = Orders.query.filter_by(status=True).order_by(Orders.id.desc()).all()
    if request.method == "POST":
        order = request.form["delete"]
        order_product = Orders.query.filter_by(product=order).first()
        db.session.delete(order_product)
        db.session.commit()
        return redirect(url_for('manage_orders_done'))
    return render_template('manage/manage_orders_realised.html', orders_list_done=orders_list_done)


@app.route('/zarządzaj/kontakt/usun/telefon/<int:id>', methods=["GET", "POST"])
def delete_contact(id):
    delete_data = Contact.query.filter_by(id=id).first()
    status = "contact"
    if request.method == "POST":
        if request.form['delete']:
            db.session.delete(delete_data)
            db.session.commit()
            return redirect(url_for("manage_contact"))
        else:
            flash('Co poszło nie tak', category='danger')
    return render_template("delete/delete_contact_data_confirmation.html", delete_data=delete_data, status=status)


@app.route('/zarządzaj/kontakt/edytuj/telefon/<int:id>', methods=["GET", "POST"])
def edit_contact(id):
    edit_data = Contact.query.filter_by(id=id).first()
    status = "contact"
    form = ContactForm()
    if form.validate_on_submit():
        edit_data.phone_number = form.phone_number.data
        edit_data.number_owner  = form.number_owner.data
        db.session.commit()
        return redirect(url_for("manage_contact"))
    return render_template("manage/manage_edit_contact_data.html", status=status, edit_data=edit_data, form=form)


@app.route('/zarządzaj/kontakt/usun/adres/<int:id>', methods=["GET", "POST"])
def delete_addres(id):
    delete_data = Adres.query.filter_by(id=id).first()
    status = "addres"
    if request.method == "POST":
        if request.form['delete']:
            db.session.delete(delete_data)
            db.session.commit()
            return redirect(url_for("manage_contact"))
        else:
            flash('Co poszło nie tak', category='danger')
            return redirect(url_for("manage_contact"))
    return render_template("delete/delete_contact_data_confirmation.html", delete_data=delete_data, status=status)


@app.route('/zarządzaj/kontakt/edytuj/adres/<int:id>', methods=["GET", "POST"])
def edit_addres(id):
    edit_data = Adres.query.filter_by(id=id).first()
    status = "addres"
    form = AdresForm()
    if form.validate_on_submit():
        edit_data.addres = form.addres.data
        db.session.commit()
        return redirect(url_for("manage_contact"))
    return render_template("edit_contact_data.html", status=status, edit_data=edit_data, form=form)


@app.route('/zarządzaj/kontakt/usun/social/<int:id>', methods=["GET", "POST"])
def delete_social(id):
    delete_data = SocialMedia.query.filter_by(id=id).first()
    status = "social"
    if request.method == "POST":
        if request.form['delete']:
            db.session.delete(delete_data)
            db.session.commit()
            return redirect(url_for("manage_contact"))
        else:
            flash('Co poszło nie tak', category='danger')
    return render_template("delete/delete_contact_data_confirmation.html", delete_data=delete_data, status=status)


@app.route('/zarządzaj/kontakt/edytuj/social/<int:id>', methods=["GET", "POST"])
def edit_social(id):
    edit_data = SocialMedia.query.filter_by(id=id).first()
    status = "social"
    form = SocialMediaForm()
    if form.validate_on_submit():
        print("ok")
        edit_data.social_media_link = form.social_media_link.data
        edit_data.media  = form.media.data
        db.session.commit()
        return redirect(url_for("manage_contact"))
    return render_template("edit_contact_data.html", status=status, edit_data=edit_data, form=form)


@app.route('/kotakt')
def contact():
    addreses = Adres.query.all()
    phone_numbers = Contact.query.all()
    links = SocialMedia.query.all()
    return render_template('contact.html', addreses=addreses, phone_numbers=phone_numbers, links=links)
    













