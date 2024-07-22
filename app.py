from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    initial = True
    user_input = request.args.get('user_input', '')
    suggestions = []

    if user_input:
        suggestions = [book for book in pt.index if user_input.lower() in book.lower()]

    all_books = list(pt.index)  # Get all book titles

    return render_template('recommend.html', initial=initial, user_input=user_input, suggestions=suggestions, data=[], all_books=all_books)

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    similar_items = []
    message = None

    if user_input in pt.index:
        index = pt.index.get_loc(user_input)
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
        
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
    else:
        message = "The book is not in the database."
        data = []

    all_books = list(pt.index)  # Get all book titles

    return render_template('recommend.html', data=data, message=message, user_input=user_input, suggestions=[], all_books=all_books)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
