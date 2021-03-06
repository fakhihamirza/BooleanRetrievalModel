import nltk
import string
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import os
import sys
import ast

stopwords_file = open('Stopword-List.txt', errors="ignore").read()
stopwords = nltk.word_tokenize(stopwords_file)


stemmed_tokens=[]
Inverted_Index = {}
Positional_Index = {}
ps = PorterStemmer()

def Pre_processing():
    #for all documents in corpus-open file and read
    # f= open("stemmed.txt", "w")
    for doc_num in range(1,51):
        file_name = str(doc_num) + ".txt"
        content = open(file_name,"r",encoding = "utf-8", errors="ignore").read()
        content=content.lower()      #TO LOWER

        #Remove punctuations and tokenize
        regex = re.compile('[^a-zA-Z0-9\s]')
        content = re.sub(regex,' ',content)
        regex = re.compile('[-]')
        content = re.sub(regex,' ',content)
        tokens = nltk.word_tokenize(content)   

        #Stemming
        stemmed_tokens=[ps.stem(word) for word in tokens]

        #Creating Positional and Inverted Indexes
        word_position = 0
        for word in stemmed_tokens: 
            # f.write(word + '\n')
            if word not in stopwords:
                if word not in Inverted_Index:
                    Inverted_Index[word]=[]
                if word in Inverted_Index:
                    if Inverted_Index[word].count(doc_num)<=0:
                        Inverted_Index[word].append(doc_num)
                if word in Positional_Index:
                    if doc_num in Positional_Index[word]:
                        Positional_Index[word][doc_num].append(word_position)
                    else:
                        Positional_Index[word][doc_num] = [word_position]
                else:
                    Positional_Index[word] ={doc_num: [word_position]}
            word_position=word_position + 1
    # f.close()

# Writing indexes to file //not needed anymore//
def write_to_file():
    f = open("inverted.txt","w")
    f.write( str(Inverted_Index) )
    f.close()

    f = open("positional.txt","w")
    f.write( str(Positional_Index) )
    f.close()

#to avoid multiple pre processing
def read_from_file():
    file = open("inverted.txt","r")
    contents = file.read()
    Inverted_Index = ast.literal_eval(contents)
    file.close()
    # print(type(Inverted_Index))
    file = open("positional.txt","r")
    contents = file.read()
    Positional_Index=ast.literal_eval(contents)
    print(type(Positional_Index))
    file.close()
    with open("stemmed.txt", 'r') as f:
        stemmed_tokens = [line.rstrip('\n') for line in f]
    for s in stemmed_tokens:
        print(s)
    f.close()

def Boolean_Query(query):
    f_and=0
    f_or=0
    f_not=0

    #Preprocessing Query
    query=query.lower() 
    regex = re.compile('[^a-zA-Z0-9\s]')
    query = re.sub(regex,' ',query)
    regex = re.compile('[-]')
    query = re.sub(regex,' ',query)

    result = []
    p1=[]
    p2=[]
    p3=[]

    #Boolean Logic Implemented
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
    result = p1[0]
    return result

def Proximity_Query(query):
    #Pre processing Query
    query=query.lower()    
    regex = re.compile('[^a-zA-Z0-9\s]')
    query = re.sub(regex,' ',query)
    regex = re.compile('[-]')
    query = re.sub(regex,' ',query)

    result = []
    p1=[]
    p2=[]
    
    #Proximity logic Implemented
    query_list = nltk.word_tokenize(query)  
    print(query_list)
    for doc_num in range(1,51):  
        word = query_list[0]
        word2 = query_list[1]
        word=ps.stem(word)
        word2=ps.stem(word2)
        if doc_num in Positional_Index[word] and doc_num in Positional_Index[word2]:
            if word in Positional_Index:
                p1=Positional_Index[word][doc_num]
            if word2 in Positional_Index:
                p2 = Positional_Index[word2][doc_num]
            for i in p1:
                for j in p2:
                    if j-(int(query_list[2])+1) == j:
                        print(doc_num)
                        result.append(doc_num)
                    if i+(int(query_list[2])+1) == j:
                        print(doc_num)
                        result.append(doc_num)
    return(result)

#Main
def model (query):
    #if no changes, can use prev made indexes hence
    # read_from_file()
    if query.find("/") != -1:
        Result = Proximity_Query(query)
    else:
        Result = Boolean_Query(query)
        Result = list(Result)
    print(Result)
    return Result

def pre():
    Pre_processing()