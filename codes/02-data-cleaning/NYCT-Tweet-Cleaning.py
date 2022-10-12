# Import relevant packages
import pandas as pd
import numpy as np
import nltk
import os
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from wordcloud import WordCloud
import seaborn as sns
from matplotlib import pyplot as plt

# Set working directory to current file location
wdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(wdir)

# Import NYCT Tweet Data Set and Combine all separate searches
nyct_base = pd.read_csv("../../data/00-raw-data/NYCTSubway-Tweets-0901-0914.csv",index_col=0,encoding="unicode_escape")
### COMBINE DATAFRAMES AND SAVE ###
base_path = os.listdir("../../data/00-raw-data")
nyct = pd.DataFrame(columns=nyct_base.columns)
for f in base_path:
    if f.startswith('NYCTSubway'):
        new_df = pd.read_csv("../../data/00-raw-data/"+ f,index_col=0,encoding="unicode_escape")
        nyct = pd.concat([nyct,new_df],axis=0)
print(nyct.head())


# Define stop words
mystopwords = stopwords.words('english')
# Remove stop words with length 1 (subway line names are 1 letter)
mystopwords = [word for word in mystopwords if len(word)>1]
# Append frequently used words from NYCT twitter that are not useful for analysis
mystopwords.extend(["Northbound","Southbound","southbound","northbound","both","directions","while","running","problems","delays","delayed","delay","st","ave","av","rd","train","trains","near",'i','d','s','t','need'])

# Convert text of tweets to list
tweets = nyct['text'].tolist()
# Remove urls from text
tweets = [re.sub(r'http\S+', '', x) for x in tweets]
# Use CountVectorizer to tokenize tweets
nyct_cvec = CountVectorizer(stop_words=mystopwords)
nyct_mx = nyct_cvec.fit_transform(tweets)
nyct_array = nyct_mx.toarray()
# Create document term frequency matrix
nyct_dtm = pd.DataFrame(data=nyct_array,columns=nyct_cvec.get_feature_names_out())
# Save dtm to csv
#nyct_dtm.to_csv('../../data/01-modified-data/NYCT-0901-0914-tweets-DTM.csv')
nyct_dtm.to_csv('../../data/01-modified-data/NYCT-tweets-DTM.csv')

### PROCESSING FOR LINE LETTERS ###
tweets = [tweet.replace('/',' ') for tweet in tweets]
tweets_one_mod = []
subway_line_list = ['1','2','3','4','5','6','7','A','B','C','D','E','F','G','J','L','M','N','Q','R','S','W','Z']
# Remove all words in tweet with length greater than 1
for tweet in tweets:
    word_list = tweet.split(" ")
    new_words = [word for word in word_list if len(word)==1]
    # Filter out lower case letters
    new_words = [word for word in new_words if word.isupper() or word.isnumeric()]
    # Filter out invalid letters/numbers (ones that are not subway lines)
    new_words = [word for word in new_words if word in subway_line_list]
    new_word_str = ' '.join(new_words)
    tweets_one_mod.append(new_word_str)
# Remove empty strings
tweets_one_mod = [tweet for tweet in tweets_one_mod if tweet]
# Vectorize and create DTM
regex = '^[a-zA-Z0-9]*$'
one_vec = CountVectorizer(token_pattern=regex,lowercase=False)
one_mod_mx = one_vec.fit_transform(tweets_one_mod)
one_mod_array = one_mod_mx.toarray()
one_mod_dtm = pd.DataFrame(data=one_mod_array,columns=one_vec.get_feature_names_out())
# Save t csv
#one_mod_dtm.to_csv('../../data/01-modified-data/one-char-0901-0914-tweets-DTM.csv')
one_mod_dtm.to_csv('../../data/01-modified-data/one-char-tweets-DTM.csv')


'''
#EDA Testing for Stop Words
# Word Cloud
vocab1 = nyct_dtm.T.sum(axis=1)
nyct_wc = WordCloud(max_words=50).generate_from_frequencies(vocab1)
plt.imshow(nyct_wc)
plt.axis('off')
plt.show()

vocab2 = one_mod_dtm.T.sum(axis=1)
one_mod_wc = WordCloud(max_words=50,background).generate_from_frequencies(vocab2)
plt.imshow(one_mod_wc)
'''