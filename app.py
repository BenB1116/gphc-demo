from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db = SQLAlchemy(app)

class Checkouts(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True, nullable = False)
    item_id = db.Column(db.Integer, primary_key=True, nullable = False)

class Inventory(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    author_last = db.Column(db.String(100), nullable = False)
    author_first = db.Column(db.String(100), nullable = False)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
