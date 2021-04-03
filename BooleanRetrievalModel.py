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

stopwords_file = open('Stopword-List.txt', errors="ignore").read()
stopwords = nltk.word_tokenize(stopwords_file)

stemmed_tokens=[]
Inverted_Index = {}
Positional_Index = {}

for doc_num in range(1,51):
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
                #Positional_Index[word].append({doc_num:word_position})
                Positional_Index[word][doc_num] = [word_position]
        else:
            #Positional_Index[word] = []
            Positional_Index[word] ={doc_num: [word_position]}
            #Positional_Index[word].append({doc_num:word_position})
        word_position=word_position + 1
f = open("inverted.txt","w")
f.write( str(Inverted_Index) )
f.close()

f = open("positional.txt","w")
f.write( str(Positional_Index) )
f.close()

def Boolean_Query(query):
    f_and=0
    f_or=0
    f_not=0
    query=query.lower()    
    punctuationRe = "[.,!?:;‘’”“\"]"
    query = re.sub(punctuationRe, "", query)
    query = re.sub("[-]", " ", query)

    result = []
    p1=[]
    p2=[]
    p3=[]

    query_list = nltk.word_tokenize(query)  
    print(query_list)
    i=0
    for word in query_list:
        if word =='and':
            f_and = 1
        elif word == 'or':
            f_or = 1
        elif word == 'not':
            f_not = 1
        else:
            word=ps.stem(word)
            if f_not:
                if word in Inverted_Index:
                    temp=[]
                    temp2=[]
                    temp = Inverted_Index.get(word)
                    for i in range (1,51):
                        if i not in temp:
                            temp2.append(i)
                    p1.append(temp2)
                    if f_and:
                        p1[0] = set(p1[0]).intersection(p1[1])
                        p1.pop()
                        f_and = 0
                    if f_or:
                        p1[0] = set(p1[0]).union(p1[1])
                        p1.pop()
                        f_or = 0
                else:
                    p1.append([])
                f_not=0
            elif not f_and and not f_or and not f_not:
                if word in Inverted_Index:
                    p1.append(Inverted_Index.get(word))
                else:
                    p1.append([])
            elif f_and:
                if word in Inverted_Index:
                    p1.append(Inverted_Index.get(word))
                else:
                    p1.append([])
                p1[0] = set(p1[0]).intersection(p1[1])
                p1.pop()
                f_and=0
            elif f_or:
                if word in Inverted_Index:
                    p1.append(Inverted_Index.get(word))
                else:
                    p1.append([])
                p1[0] = set(p1[0]).union(p1[1])
                p1.pop()
                f_or=0
    print(p1)


# def positional_query(query):
while(s != 4):
    query = input("Enter your query!")
    Boolean_Query(query)
    s=input()
