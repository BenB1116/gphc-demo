from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Create and configure the app
app = Flask(__name__)

# Read in csvs as DataFrames
patron_df = pd.read_csv('data\clean\patron_data.csv')
inv_df = pd.read_csv('data\clean\inv_data.csv')

# Drop duplicates from patron_df
patron_df.drop_duplicates(inplace=True)

# Create a matrix of the vectorized titles from inv_df
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(inv_df['title'])

# Search returns the closest title to an searched title
def search_for_title(query):
    # Remove special characters and convert into a vector
    proccessed = re.sub('[^a-zA-Z0-9 ]', '', query.lower())
    query_vec = vectorizer.transform([proccessed])

    # Compare query vector against vectorized titles and select the top 1
    # This can be modified to return top n results
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    index = np.argpartition(similarity, -1)[-1:]
    result = inv_df.loc[index[0]]

    return result

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        searched_title = request.form['title']
        try:
            return search_for_title(searched_title)
        except:
            return 'There was an issue'
    else:
        return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
