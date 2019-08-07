import pandas as pd
from preprocess import *
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import time
from sklearn.metrics import precision_recall_fscore_support as score
import pickle


data=pd.read_csv('headlines.txt',sep='#',header=None)
data.columns = ["body_text", "label"]
negData = data.loc[data['label'] == 'neg']

# find negative words and positive words count for it
data['negCount'] = data['body_text'].apply(lambda x: negCount(x))
data['posCount'] = data['body_text'].apply(lambda x: posCount(x))
data = shuffle(data)

X_train, X_test, y_train, y_test = train_test_split(data[['body_text','negCount']], data['label'], test_size=0.2)

tfidf_vect = TfidfVectorizer(analyzer=clean_text, ngram_range =(1,5),use_idf = False)
tfidf_vect_fit = tfidf_vect.fit(X_train['body_text'])

tfidf_train = tfidf_vect_fit.transform(X_train['body_text'])
tfidf_test = tfidf_vect_fit.transform(X_test['body_text'])

#pickle.dump(tfidf_vect_fit, open('vector.sav', 'wb'))

X_train_vect = pd.concat([X_train[['negCount']].reset_index(drop=True),
           pd.DataFrame(tfidf_train.toarray())], axis=1)
X_test_vect = pd.concat([X_test[['negCount']].reset_index(drop=True),
           pd.DataFrame(tfidf_test.toarray())], axis=1)


def train_rfc(x, y):

    rf = RandomForestClassifier(n_estimators=500, max_depth=None, n_jobs=-1)
    start = time.time()
    rf_model = rf.fit(x, y)
    end = time.time()
    fit_time = end - start
    return rf_model, fit_time


def train_gb(x, y):

    gb = GradientBoostingClassifier(n_estimators=250, max_depth=31, learning_rate = 0.05, random_state=10,
                                    max_features='sqrt',subsample = 0.95)
    start = time.time()
    gb_model = gb.fit(x, y)
    end = time.time()
    fit_time = end - start
    return gb_model, fit_time


def main():
    model,fit_time = train_gb(X_train_vect, y_train)

    start = time.time()
    y_pred = model.predict(X_test_vect)
    end = time.time()
    pred_time = end - start

    precision, recall, fscore, train_support = score(y_test, y_pred, pos_label='neg', average='binary')
    print('Fit time: {} / Predict time: {} ---- Precision: {} / Recall: {} / Accuracy: {}'.format(
        round(fit_time, 3), round(pred_time, 3), round(precision, 3), round(recall, 3),
        round((y_pred == y_test).sum() / len(y_pred), 3)))

    #pickle.dump(gb_model, open('gbc.sav', 'wb'))

if __name__=='__main__':
    main()
