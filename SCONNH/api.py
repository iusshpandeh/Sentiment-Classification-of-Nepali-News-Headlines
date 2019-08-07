import flask
from flask import render_template, url_for, redirect
from flask import Blueprint
from preprocess import *
import pickle
import pandas as pd
import numpy as np
rf_model=pickle.load(open('final_gbc.sav', 'rb'))

from bs4 import BeautifulSoup
import requests
import os,io
import bs4 as bs
import urllib.request




app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/')
def homepage():
        return render_template('index.html')




@app.route('/nagarik')
def nagarik():
    ts = []
    pos_news = []
    neg_news = []
    pos_link = []
    neg_link = []
    nlink = []
    link = "https://nagariknews.nagariknetwork.com/news/"
    for i in range(80702, 80720):
        source_link = link + str(i)

        source_code = requests.get(source_link).text
        soup = BeautifulSoup(source_code, 'html.parser')
        headlines = soup.find('div', class_='inner-section cover-news')
        headline = headlines.find('h1')
        h1 = headline.text[0:100]

        ts.append([h1])
        nlink.append([source_link])
    # print(ts)


    testDf = pd.DataFrame(ts)
    tfidf_vect_fit = pickle.load(open("final_vector.sav", 'rb'))
    testDf.columns = ["text"]
    testDf['negCount'] = testDf['text'].apply(lambda x: negCount(x))
    testDf['posCount'] = testDf['text'].apply(lambda x: posCount(x))
    tfidf_test = tfidf_vect_fit.transform(testDf['text'])
    X_test_vect = pd.concat([testDf[['negCount','posCount']].reset_index(drop=True),
                             pd.DataFrame(tfidf_test.toarray())], axis=1)
    y_pred = rf_model.predict(X_test_vect)
    for i in range(len(y_pred)):
        if y_pred[i]=="pos":
            pos_news.append(ts[i][0])
            pos_link.append(nlink[i][0])
            pos_length=len(pos_news)

        else:
            neg_news.append(ts[i][0])
            neg_link.append(nlink[i][0])
            neg_length = len(neg_news)

    return render_template('detail.html',pos_news=pos_news,neg_news=neg_news,pos_link=pos_link,neg_link=neg_link,pos_length=pos_length,neg_length=neg_length)



@app.route('/setopati')
def setopati():
    ts = []
    pos_news = []
    neg_news = []
    pos_link = []
    neg_link = []
    nlink = []
    link = "https://www.setopati.com/politics/"
    for i in range(187111, 187131):
        source_link = link + str(i)
        # print(source_link)
        source_code = requests.get(source_link).text
        soup = BeautifulSoup(source_code, 'html.parser')
        headlines = soup.find('div', class_='title-names col-md-10 offset-md-2')
        #     print(headlines)
        headline = headlines.find('span', class_='news-big-title')
        #     print(headline)
        h1 = headline.text[0:100]

        ts.append([h1])
        nlink.append([source_link])
    # print(ts)


    testDf = pd.DataFrame(ts)
    tfidf_vect_fit = pickle.load(open("final_vector.sav", 'rb'))
    testDf.columns = ["text"]
    testDf['negCount'] = testDf['text'].apply(lambda x: negCount(x))
    testDf['posCount'] = testDf['text'].apply(lambda x: posCount(x))
    tfidf_test = tfidf_vect_fit.transform(testDf['text'])
    X_test_vect = pd.concat([testDf[['negCount','posCount']].reset_index(drop=True),
                             pd.DataFrame(tfidf_test.toarray())], axis=1)
    y_pred = rf_model.predict(X_test_vect)
    for i in range(len(y_pred)):
        if y_pred[i]=="pos":
            pos_news.append(ts[i][0])
            pos_link.append(nlink[i][0])
            pos_length=len(pos_news)

        else:
            neg_news.append(ts[i][0])
            neg_link.append(nlink[i][0])
            neg_length = len(neg_news)

    return render_template('detail.html',pos_news=pos_news,neg_news=neg_news,pos_link=pos_link,neg_link=neg_link,pos_length=pos_length,neg_length=neg_length)


@app.route('/kantipur')
def kantipur():
    ts = []
    pos_news = []
    neg_news = []
    pos_link = []
    neg_link = []
    nlink = []
    def header():
        source = urllib.request.urlopen('http://www.ekantipur.com/').read()

        soup = bs.BeautifulSoup(source, 'lxml')
        data = [[]]

        for paragraph in soup.find_all('div', class_='display-news-title'):
            data.append([paragraph.text, paragraph.a.get('href')])
        return data

    ekantipur = header()
    for i in range(1,len(ekantipur)):
        ts.append(ekantipur[i][0])
        nlink.append(ekantipur[i][1])

    testDf = pd.DataFrame(ts)
    tfidf_vect_fit = pickle.load(open("final_vector.sav", 'rb'))
    testDf.columns = ["text"]
    testDf['negCount'] = testDf['text'].apply(lambda x: negCount(x))
    testDf['posCount'] = testDf['text'].apply(lambda x: posCount(x))
    tfidf_test = tfidf_vect_fit.transform(testDf['text'])
    X_test_vect = pd.concat([testDf[['negCount', 'posCount']].reset_index(drop=True),
                             pd.DataFrame(tfidf_test.toarray())], axis=1)
    y_pred = rf_model.predict(X_test_vect)
    for i in range(len(y_pred)):
        if y_pred[i] == "pos":
            pos_news.append(ts[i])
            pos_link.append(nlink[i])
            pos_length = 8

        else:
            neg_news.append(ts[i])
            neg_link.append(nlink[i])
            neg_length = 8

    return render_template('detail.html', pos_news=pos_news, neg_news=neg_news, pos_link=pos_link, neg_link=neg_link,
                           pos_length=pos_length, neg_length=neg_length)


app.run()
