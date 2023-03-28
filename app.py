from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from knn import knn
from titlecase import titlecase

# Create and configure the app
app = Flask(__name__)

# Read in csvs as DataFrames
patron_df = pd.read_csv('data\clean\patron_data.csv')
inv_df = pd.read_csv('data\clean\inv_data_gr.csv')

# Drop duplicates from patron_df
patron_df.drop_duplicates(inplace=True)

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

def search_by_index(index):
    # Find the index in the inventory
    result = inv_df[inv_df['item_id'] == index]
    result = result.to_dict('records')[0]
    result['title'] = titlecase(result['title'])

    # Return the item in the form of a dictionary
    return result

print(inv_df.head())

ids_list = []
items_dict_list = []

@app.route('/', methods=['POST', 'GET'])
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
            print(ids_list)

            # return item_dict['title']
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('index.html', items = items_dict_list)
    
# Create a new knn object
new_knn = knn(patron_df, 3, n)

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
