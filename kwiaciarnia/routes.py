from flask import render_template, redirect, url_for
from kwiaciarnia import app
from kwiaciarnia import db
# oK5XKfRTkmBZShUafzZF
@app.route('/oK5XKfRTkmBZShUafzZF')
def stworz():
    db.create_all()
    return "weszło"

@app.route("/")
def home():
    return render_template('index.html')


@app.errorhandler(404)
def invalid_route(e):
    return 'Wprowadszono niepoprawny adres'

