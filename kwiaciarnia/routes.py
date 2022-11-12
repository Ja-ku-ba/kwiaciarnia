from flask import render_template
from kwiaciarnia import app

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.errorhandler(404)
def invalid_route(e):
    return 'Wprowadszono niepoprawny adres'

