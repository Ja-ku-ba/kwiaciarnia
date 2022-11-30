from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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