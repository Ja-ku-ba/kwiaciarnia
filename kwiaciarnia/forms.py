from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class PostForm(FlaskForm):
    title = StringField(label="Nagłówek: ")
    body = StringField(label="Treść postu: ")
    submit = SubmitField(label="Potwierdź")