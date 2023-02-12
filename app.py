from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, Form
from wtforms.validators import DataRequired, Length
import pandas as pd

# Create and configure the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

app.app_context().push()


class SearchForm(Form):  # create form
    title = StringField('Inventory', validators=[DataRequired(), Length(
        max=40)], render_kw={"placeholder": "title"})


# Create the database schema
class Checkout(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)


class Inventory(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author_last = db.Column(db.String(100), nullable=False)
    author_first = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {'title': self.title}


# Fill the database with data from csvs
with open(r'C:\Users\Ben\Desktop\hrp-machine-learning\data\clean\patron_data.csv', 'r') as file:
    patron_df = pd.read_csv(file)
patron_df.to_sql('Checkout', con=db.engine, if_exists='replace')

with open(r'C:\Users\Ben\Desktop\hrp-machine-learning\data\clean\inv_data.csv', 'r') as file:
    inv_df = pd.read_csv(file)
inv_df.to_sql('Inventory', index=False, con=db.engine, if_exists='replace')


@app.route('/')
def index():
    form = SearchForm(request.form)
    return render_template('index.html', form=form)


@app.route('/titles')
def titledic():
    res = Inventory.query.all()

    list_titles = [r.as_dict() for r in res]
    return jsonify(list_titles)


@app.route('/process', methods=['POST'])
def process():
    title = request.form['title']
    if title:
        return jsonify({'title': title})
    return jsonify({'error': 'missing data..'})


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
