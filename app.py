from tkinter.ttk import Separator
from flask import Flask, render_template, request, Response, redirect 
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app =Flask(__name__)


# @app.route('/')
# def hello():
#     return render_template('base.html')


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        df = pd.read_csv(r"C:\Users\vaibhav09\Desktop\Labs\webx\static\movies.csv")
        df.head()

        df.shape

        #selecting the column  based on featurefor prediction

        selected_features = ['genres',  'keywords', 'tagline', 'cast', 'director']
        print(selected_features)

        #filling the null value with null string
        for feature in selected_features:
            df[feature] = df[feature].fillna('')

        #creating new df for operations 
        combined_features = df['genres']+' '+df[ 'keywords']+' '+df['tagline']+' '+df['cast']+ ''+df['director'] 
        combined_features

        #covering string data to numerical data
        vectorizer = TfidfVectorizer()

        feature_vectors = vectorizer.fit_transform(combined_features)

        print(feature_vectors)

        #cosine similarity score

        similarity = cosine_similarity(feature_vectors)
        print(similarity)

        print(similarity.shape)

        #getting input from user

        # movie_name = input('Enter Movie Name  : ')

        # #creating list similar to input

        # list_of_all_titles = df['title'].tolist()
        # print(list_of_all_titles)

        # # finding the close match for the movie name given by the user

        # find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        # print(find_close_match)

        # #getting exact match

        # close_match = find_close_match[0]
        # print(close_match)

        # # finding the index of the movie with title

        # index_of_the_movie = df[df.title == close_match]['index'].values[0]
        # print(index_of_the_movie)

        # # getting a list of similar movies

        # similarity_score = list(enumerate(similarity[index_of_the_movie]))
        # print(similarity_score)

        # len(similarity_score)

        # # sorting the movies based on their similarity score

        # sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
        # print(sorted_similar_movies)


        movie_name = request.form.get("searched_movie")
        #movie_name = input(' Enter your favourite movie name : ')

        list_of_all_titles = df['title'].tolist()

        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

        close_match = find_close_match[0]

        index_of_the_movie = df[df.title == close_match]['index'].values[0]

        similarity_score = list(enumerate(similarity[index_of_the_movie]))

        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

        
        i = 1
        sugested_movies = []
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = df[df.index==index]['title'] 
            if (i<16):
                names_movies = list(title_from_index)
                i+=1
                sugested_movies += names_movies
            
        return render_template('index.html',sugested_movies=sugested_movies,close_match=close_match, movie_name=movie_name )
    return render_template('index.html')
#,data=movie_name
if __name__ == '__main__':
    app.run(debug=True)