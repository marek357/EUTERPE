# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:56:26 2020

@author: Antek
"""

import pandas as pd

def clear_non_ascii(text):
    return "".join(i for i in text if ord(i)<128)

def clear_brackets(text):
    start = text.find('[')
    while start != -1:
        #print(start)
        start += 1  # skip the bracket, move to the next character
        end = text.find(']', start)
        if end != -1:
            text = text[0:start-1] + text[end+1:len(text)]
        else:
            text = text[0:start-1] + text[start:len(text)]
        start = text.find('[')
    return text
def lower_case(text):
    return text.lower()
def is_english(text):
    flag = False
    common_words = ["you", "and", "have","like", "from", "which", "what", "they", "said", "then", "with", "look", "here"]
    for word in common_words:
        if word in text:
            flag = True
    return flag

data = pd.read_csv('songs_dataset.csv')
genres = ["Rap", "Hip-Hop", "Pop","Rock","Indie", "Country","Blues","Folk","Punk","Soul","Metal"]

lyrics = []
N = data.shape[0]

for gen in genres:
    for i in range(N):
        if i%10000 == 0:
            print(i)
        if gen in data['Genre'][i]:
            lyr = data['Lyrics'][i]
            if is_english(lyr):
                lyr = lower_case(lyr)
                lyr = clear_brackets(lyr)
                lyr = clear_non_ascii(lyr)
                lyrics.append(lyr)
    print(gen, len(lyrics))
    print(lyrics[0])
    f= open(gen+".txt","a+")
    for text in lyrics:
        f.write(text)
    f.close()
    lyrics.clear()

    
    