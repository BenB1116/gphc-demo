from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Create and configure the app
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db = SQLAlchemy(app)

# app.app_context().push()

# # Create the database schema
# class Checkout(db.Model):
#     index = db.Column(db.Integer, primary_key=True)
#     patron_id = db.Column(db.Integer, nullable=False)
#     item_id = db.Column(db.Integer, nullable=False)


# class Inventory(db.Model):
#     item_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     title = db.Column(db.String(100), nullable=False)
#     author_last = db.Column(db.String(100), nullable=False)
#     author_first = db.Column(db.String(100), nullable=False)


# # Fill the database with data from csvs
# with open(r'C:\Users\Ben\Desktop\hrp-machine-learning\data\clean\patron_data.csv', 'r') as file:
#     patron_df = pd.read_csv(file)
# patron_df.to_sql('Checkout', con=db.engine, if_exists='replace')

# with open(r'C:\Users\Ben\Desktop\hrp-machine-learning\data\clean\inv_data.csv', 'r') as file:
#     inv_df = pd.read_csv(file)
# inv_df.to_sql('Inventory', index=False, con=db.engine, if_exists='replace')

patron_df = pd.read_csv('data\clean\patron_data.csv')
inv_df = pd.read_csv('data\clean\inv_data.csv')

patron_df.drop_duplicates(inplace=True)

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(inv_df['title'])

def search_for_title(query):
    proccessed = re.sub('[^a-zA-Z0-9 ]', '', query.lower())
    query_vec = vectorizer.transform([proccessed])
    similarity = cosine_similarity(query_vec, tfidf).flatten()

    index = np.argpartition(similarity, -1)[-1:]
    result = str(inv_df.iloc[index]['title'])

    return result

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        searched_title = request.form['title']
        try:
            # searched_item = Inventory.query.filter_by(title = title).first()
            return search_for_title(searched_title)
        except:
            return 'There was an issue'
    else:
        return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
