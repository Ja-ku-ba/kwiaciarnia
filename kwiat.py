from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kwiaciarnia.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text())
    def __repr__(self):
        return self.body()

@app.route("/")
def hello_world():
    return render_template('index.html', cos=db)

if __name__=="__main__":
    app.run(debug=True)


