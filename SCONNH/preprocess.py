import re
import string
from nepali_tokenize import nepali_tokenize
from stemmer import stemword

#regex to remove nepali number
nepali_num = re.compile(r'(०|१|२|३|४|५|६|७|८|९)+')

#load stopwords
stopwords = open('nepali_stopwords.txt','r',encoding="utf-8").read().splitlines()

#load negative words
negWords = open('neg.csv','r', encoding="utf-8").read().splitlines()

#load positive words
posWords = open('positive_words.txt','r', encoding="utf-8").read().splitlines()

'''

clean_text function:
1. removes punctuation
2. tokenizes the text
3. removes numbers
4. removes stopwords
5. stems the words
6. returns the cleaned text

'''
def clean_text(text):
    text = "".join([word for word in text if word not in string.punctuation])
    tokens = nepali_tokenize(text)
    text_no_num = [token for token in tokens if  not nepali_num.match(token)]
    text = [stemword(word) for word in text_no_num if word not in stopwords]
    return text


#returns the percent of negative terms
def negCount(text):
    text = clean_text(text)
    count = sum([1 for word in text if word in negWords])
    return round(count/(len(text) - text.count(" ")), 3)

#returns the percent of positive terms
def posCount(text):
    text = clean_text(text)
    count = sum([1 for word in text if word in posWords])
    return round(count/(len(text) - text.count(" ")), 3)

