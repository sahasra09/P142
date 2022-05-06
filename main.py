from flask import Flask,jsonify,request
import csv 
from demographic_filtering import output
from content_filtering import get_recommendations

all_articles=[]
with open('articles.csv',encoding='utf-8') as f:
    reader=csv.reader(f)
    data=list(reader)
    all_articles=data[1:]
liked_articles=[]
not_liked_articles=[]
app=Flask(__name__)
@app.route('/get-article')
def get_article():
    return jsonify({
        'data':all_articles[0],
        'status':'success',
    })

@app.route('/liked-article',methods=['POST'])
def liked_article():
    article=all_articles[0]
    all_articles=all_articles[1:]
    liked_articles.append(article)
    return jsonify({
        'status':'success'
    }),201

@app.route('/unliked-article',methods=['POST'])
def unliked_articles():
    article=all_articles[0]
    all_articles=all_articles[1:]
    not_liked_articles.append(article)
    return jsonify({
        'status':'success'
    }),201
    
@app.route('/popular-movies')
def popular_movies():
    movie_data=[]
    for movie in output:
        d={
            'title':movie[0],
            'poster_link':movie[1],
            'release_date':movie[2] or 'N/A',
            'duration':movie[3],
            'rating':movie[4],
            'overview':movie[5]
        }
        movie_data.append(d)
    return jsonify({
        'data':movie_data,
        'status':'success'
    },200)

@app.route('/recommended_articles')
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[12])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__=='__main__':
    app.run()
