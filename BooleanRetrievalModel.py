import nltk
import string
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import glob
import os
import numpy as np
import json
import sys
from collections import defaultdict

file_name = ['1.txt','2.txt','3.txt','4.txt','5.txt','6.txt','7.txt','8.txt','9.txt','10.txt','11.txt','12.txt','13.txt','14.txt','15.txt','16.txt','17.txt','18.txt','19.txt','20.txt','21.txt','22.txt','23.txt','24.txt','25.txt','26.txt','27.txt','28.txt','29.txt','30.txt','31.txt','32.txt','33.txt','34.txt','35.txt','36.txt','37.txt','38.txt','39.txt','40.txt','41.txt','42.txt','43.txt','44.txt','45.txt','46.txt','47.txt','48.txt','49.txt', '50.txt']
filehandle=open('tokens.txt', 'w') 
stopwords_file = open('Stopword-List.txt', errors="ignore").read()
stopwords = nltk.word_tokenize(stopwords_file)

stemmed_tokens=[]
Inverted_Index = {}
Positional_Index = {}
posting_list=[]
word_position_list={}

for doc_num in range(1,5):
    file_name = str(doc_num) + ".txt"
    content = open(file_name,"r",encoding = "utf-8", errors="ignore").read()
    content=content.lower()      #TO LOWER

    punctuationRe = "[.,!?:;‘’”“\"]"
    content = re.sub(punctuationRe, "", content)
    content = re.sub("[-]", " ", content)

    tokens = nltk.word_tokenize(content)   

    tokens_filtered= [word for word in tokens if not word in stopwords]  #REMOVE STOP WORDS
    ps = PorterStemmer()
    stemmed_tokens=[ps.stem(word) for word in tokens_filtered]

    word_position = 0
    tempdict={}
    for word in stemmed_tokens: 
        if word not in Inverted_Index:
            Inverted_Index[word]=[]
        if word in Inverted_Index:
            if Inverted_Index[word].count(doc_num)<=0:
                Inverted_Index[word].append(doc_num)
        if word in Positional_Index:
            if doc_num in Positional_Index[word]:
                Positional_Index[word][doc_num].append(word_position)
            else:
                Positional_Index[word].append({doc_num:word_position})
        else:
            Positional_Index[word] = []
            Positional_Index[word].append({doc_num:word_position})
        word_position=word_position + 1


f = open("inverted.txt","w")
f.write( str(Inverted_Index) )
f.close()

f = open("positional.txt","w")
f.write( str(Positional_Index) )
f.close()
