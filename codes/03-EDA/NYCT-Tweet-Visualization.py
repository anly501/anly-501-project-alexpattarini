# Import relevant libraries
import numpy as np
import pandas as pd
import os
import re
import wordcloud
from wordcloud import WordCloud
import seaborn as sns
from matplotlib import pyplot as plt

# Set working directory to current file location
wdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(wdir)

# Load tweet data sets
full_dtm = pd.read_csv("../../data/01-modified-data/NYCT-tweets-DTM.csv")
#print(full_dtm.head())

one_char_dtm = pd.read_csv("../../data/01-modified-data/one-char-tweets-DTM.csv")
#print(one_char_dtm.head())

# Manipulate full_wc to be in a suitable format for wordcloud visualization
full_dtm_vocab = full_dtm.T.sum(axis=1)
# Remove "Unnamed: 0" row that skews results
full_dtm_vocab = full_dtm_vocab.iloc[1:]
#print(full_dtm_vocab.head())

# Creation of word cloud for full_dtm and save as png
full_wc = WordCloud(max_words=100,background_color="white").generate_from_frequencies(full_dtm_vocab)
plt.figure()
plt.imshow(full_wc,interpolation="bilinear")
plt.title("Word Cloud of @NYCTSubway Tweets 09/01/2022-09/14/2022")
plt.axis('off')
plt.savefig("../../501-project-website/images/WORDCLOUD-Full-DTM.png")
#plt.show()

# Manipulate one_char_dtm to be in a suitable format for wordcloud visualization
one_char_vocab = one_char_dtm.T.sum(axis=1)
# Remove "Unnamed: 0" row that skews results
one_char_vocab = one_char_vocab.iloc[1:]
print(one_char_vocab.head())

# Color will be determined by subway line, color function created below
# Hexadecimal colors for NYC subway lines extracted from https://en.wikipedia.org/wiki/New_York_City_Subway_nomenclature
def line_color_fun(word, font_size, position, orientation, font_path, random_state=None):
    if word=="1" or word=="2" or word=="3":
        return "#ee352e"
    elif word=="4" or word=="5" or word=="6":
        return "#00933c"
    elif word=="7":
        return "#b933ad"
    elif word=="A" or word=="C" or word=="E":
        return "#0039a6"
    elif word=="B" or word=="D" or word=="F" or word=="M":
        return "#ff6319"
    elif word=="G":
        return "#6cbe45"
    elif word=="L":
        return "#a7a9ac"
    elif word=="J" or word=="Z":
        return "#996633"
    elif word=="N" or word=="Q" or word=="R" or word=="W":
        return "#fccc0a"
    elif word=="S":
        return "#808183"
    else:
        return "black"


# Creation of word cloud for full_dtm and save as png
one_char_wc = WordCloud(background_color="white",prefer_horizontal=1).generate_from_frequencies(one_char_vocab)
one_char_wc.recolor(color_func=line_color_fun)
plt.figure()
plt.imshow(one_char_wc,interpolation="bilinear")
plt.title("Word Cloud of Subway Lines in @NYCTSubway Tweets 09/01/2022-09/14/2022")
plt.axis('off')
plt.savefig("../../501-project-website/images/WORDCLOUD-OneChar-DTM.png")
#plt.show()


# Creation of word cloud for one_char_dtm and save as png

print("done")