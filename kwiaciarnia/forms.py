from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError

class PostForm(FlaskForm):
    title = StringField(label="Nagłówek: ", validators=[DataRequired()])
    body = StringField(label="Treść postu: ", validators=[DataRequired()])
    submit = SubmitField(label="Potwierdź")

class UserForm(FlaskForm):
    username = StringField(label="Nazwa użytkownika: ", validators=[Length(min=4, max=32), DataRequired()])
    email = StringField(label='Aadres email: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Hasło: ', validators=[Length(min=8, max=64), DataRequired()])
    password2 = PasswordField(label='Potwierdzenie hasła: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Stwórz konto")

class Loginform(FlaskForm):
    email = StringField(label='Adres email: ', validators=[DataRequired()])
    password = PasswordField(label='Hasło: ', validators=[DataRequired()])
    submit = SubmitField(label="Zaloguj")

class AddProductForm(FlaskForm):
    category = StringField(label="Kategoria: ", validators=[DataRequired()])
    name = StringField(label="Nazwa: ", validators=[DataRequired()])
    description = StringField(label="Opis: ", validators=[DataRequired()])
    price = FloatField(label='Cena (xx.xx):', validators=[DataRequired()])
    submit = SubmitField(label="Dodaj")

class BuyForm(FlaskForm):
    phone_number = StringField(label="Numer telefonu: ", validators=[Length(min=9, max=12), DataRequired()])
    submit = SubmitField(label="Potwierdź zakup")


class SocialMediaForm(FlaskForm):
    social_media_link = StringField(label="Link: ", validators=[DataRequired()])
    media = StringField(label='Platforma (instagram/facebook/inne): ')
    submit = SubmitField(label="Dodaj")

class ContactForm(FlaskForm):
    phone_number = IntegerField(label="Numer telefonu: ", validators=[DataRequired()])
    number_owner = StringField(label="Właściciel: ", validators=[DataRequired()])
    submit = SubmitField(label="Dodaj")
    
class AdresForm(FlaskForm):
    addres = StringField(label="Adres: ", validators=[DataRequired()])
    submit = SubmitField(label="Dodaj")