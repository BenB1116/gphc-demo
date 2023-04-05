from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from knn import knn
from titlecase import titlecase
import os

# Create and configure the app
app = Flask(__name__)

patron_path = os.path.join('data', 'clean', 'patron_data.csv')
inv_path = os.path.join('data', 'clean', 'inv_data_gr.csv')

# Comment back in to use Good Reads data
# patron_path = os.path.join('data', 'clean', 'patron_data_gr.csv')

# Read in csvs as DataFrames
patron_df = pd.read_csv(patron_path)
inv_df = pd.read_csv(inv_path)

# Create a matrix of the vectorized titles from inv_df
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(inv_df['title'])

# Number of recommendations
n = 5

# Search returns the closest title to an searched title
def search_for_title(query):
    # Remove special characters and convert into a vector
    proccessed = re.sub('[^a-zA-Z0-9 ]', '', query.lower())
    query_vec = vectorizer.transform([proccessed])

    # Compare query vector against vectorized titles and select the top 1
    # This can be modified to return top n results
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    index = np.argpartition(similarity, -1)[-1:][0]

    return index

def search_for_title_multi(query):
    # Remove special characters and convert into a vector
    proccessed = re.sub('[^a-zA-Z0-9 ]', '', query.lower())
    query_vec = vectorizer.transform([proccessed])

    # Compare query vector against vectorized titles and select the top 1
    # This can be modified to return top n results
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    index = np.argpartition(similarity, -5)[-5:]

    return index

def search_by_index(index):
    # Find the index in the inventory
    result = inv_df[inv_df['item_id'] == index]
    result = result.to_dict('records')[0]
    result['title'] = titlecase(result['title'])

    # Return the item in the form of a dictionary
    return result

ids_list = []
items_dict_list = []

@app.route('/', methods=['POST', 'GET', 'DELETE'])
def index():
    if request.method == 'POST':
        searched_title = request.form['title']
        try:
            # Search for the id of the title
            result_id = search_for_title(searched_title)
            # Append the id to the current id list
            ids_list.append(result_id)

            # Get the item info
            item_dict = search_by_index(result_id)
            items_dict_list.append(item_dict)

            # return item_dict['title']
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('index.html', items = items_dict_list)
    
# Create a new knn object
new_knn = knn(patron_df, 3, n)

# Routes user to the recommended page
@app.route('/recommended', methods=['GET'])
def reccomend():
    # Attempt to search items 
    if request.method == 'GET':
        try:
            # Find the top n
            top_recomendations = new_knn.top_n_closest(ids_list)
            
            # Get the dictionary representation of every recommendation
            rec_dicts = []
            for rec in top_recomendations:
                rec_dicts.append(search_by_index(rec))

            # Render the template
            return render_template('recommended.html', recs=rec_dicts, n=n)
        except:
            return 'There was an issue'
    return render_template('index.html', items = {})

# Clears the current book list
@app.route('/clear', methods=['POST', 'GET', 'DELETE'])
def clear():
    # Clear all items from both lists
    global ids_list
    global items_dict_list
    ids_list = []
    items_dict_list = []
    return render_template('index.html', items = [])

# Allows autocomplete on the search bar
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    results = search_for_title_multi(search)
    results_titles = [search_by_index(index)['title'] for index in results]
    return jsonify(matching_results=results_titles)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
