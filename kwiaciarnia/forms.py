from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class PostForm(FlaskForm):
    title = StringField(label="Nagłówek: ")
    body = StringField(label="Treść postu: ")
    submit = SubmitField(label="Potwierdź")


class UserForm(FlaskForm):
    username = StringField(label="Nazwa użytkownika: ")
    email = StringField(label='Aadres email: ')
    password1 = PasswordField(label='Hasło: ')
    password2 = PasswordField(label='Potwierdzenie hasła: ')
    submit = SubmitField(label="Stwórz konto")

class Loginform(FlaskForm):
    email = StringField(label='Adres email: ')
    password = PasswordField(label='Hasło: ')
    submit = SubmitField(label="Zaloguj")