from preprocess import *
import pickle
import pandas as pd
import numpy as np


rf_model=pickle.load(open('rfc.sav', 'rb'))

testtext = [["चालकको मृत्यु"], ["विजयीलाई सम्मान गरियो"], ["विमान दुर्घटना"],
            ["आईएसले लियो श्रीलंका बम हमलाकाे जिम्मा"],
            ["जीपको ठक्करबाट पाल्पामा ज्येष्ठ नागरिकको मृत्यु"], ["नेपालको जित"], ["नेपाल ५ विकेटले पराजित"]]
testDf = pd.DataFrame(testtext)
tfidf_vect_fit = pickle.load(open("vector.sav", 'rb'))
testDf.columns = ["text"]
testDf['negCount'] = testDf['text'].apply(lambda x: negCount(x))
testDf['posCount'] = testDf['text'].apply(lambda x: posCount(x))
testDf
tfidf_test = tfidf_vect_fit.transform(testDf['text'])
X_test_vect = pd.concat([testDf[['negCount']].reset_index(drop=True),
                         pd.DataFrame(tfidf_test.toarray())], axis=1)
y_pred = rf_model.predict(X_test_vect)
for i in range(len(testtext)):
    t = np.squeeze(testtext[i])
    print("{} - {}".format(t, y_pred[i]))

