from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

# Create and configure the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

app.app_context().push()

# Create the database schema
class Checkout(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True, nullable = False)
    item_id = db.Column(db.Integer, primary_key=True, nullable = False)

class Inventory(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    author_last = db.Column(db.String(100), nullable = False)
    author_first = db.Column(db.String(100), nullable = False)

with open(r'C:\Users\Ben\Desktop\hrp-machine-learning\data\clean\patron_data.csv', 'r') as file:
    patron_df = pd.read_csv(file)
patron_df.to_sql('Checkout', con=db.engine, if_exists='replace')


@app.route('/')
def index():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
