from nltk.corpus import brown, stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
from operator import itemgetter 
import nltk.data
from string import punctuation
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import TweetTokenizer, sent_tokenize
from collections import Counter 
import statistics
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("a.txt")
data = fp.read()
sentence=nltk.sent_tokenize(data)
print(sentence)
sentences = [TweetTokenizer().tokenize(t) for t in 
sent_tokenize(data)]
print(sentences)
stopwords = stopwords.words('english')+list(punctuation)
#clean _sentences  or document
### remove white spaces and puntuation marks
temp=[]
sentence_cl=[]
for s in sentences: 
    temp=[]
    for word in s:
        if word not in stopwords:
            temp.append(word)
    sentence_cl.append(temp)   
sentence_cl
def count_words(sen):
    count=0
    i=0
   
    for w in sen:
         count+=1
        
    return(count)#COUNT OF KEYWORDS IN A SENTENCE
def make_doc(sentence):
    doc=[]
    i=0
    for sen in sentence:
        i+=1
        count=count_words(sen)
        temp={'doc_id': i,'doc_count':count};
        doc.append(temp);
    return doc
    doc=make_doc(sentence_cl)
print(doc)# doc_id=document number 
          #doc_count=count of words in each document
print(type(doc))
## not needed as we already have cleasn sentences which contain all the info regarding this
def find_freq(sent):
    freq_doc_list={} # my method
    i=1
    for s in sentence_cl: 
        c=Counter(s)
        freq_doc_list[i]=c
        i+=1
    return freq_doc_list 
           #words=word_tokenize(sent)# tokenising the sentence 
           
freq_doc_dict=find_freq(sentence_cl)
print(freq_doc_dict)     
m=len(freq_doc_list)  # my_method
cal_tf={}#caluclated tf value to be stored in dictonary 
 
for i in freq_doc_list:
    tf={}  #dictonary that contain tf value for each document 
    for word in freq_doc_list[i]:
        n=len(freq_doc_list[i])
        tf[word]=freq_doc_list[i][word]/n #dictonary that contain tf value for each document 
        
    cal_tf[i]=tf
cal_tf
import math
m=len(freq_doc_list)  # my_method
cal_idf={}#caluclated tf value to be stored in dictonary 
c=0
idf={}
for i in freq_doc_list:  
    c+=1
    idf={}
    for word in freq_doc_list[i].keys():
        count=sum([word in temp_dict for i in freq_doc_list for temp_dict in   freq_doc_list[i] ])
        idf[word]=math.log(m/count)
    cal_idf[c]=idf

cal_idf
cal_tf_idf={}  # my_method
for i in freq_doc_list: 
    tf_idf={}
    for word in freq_doc_list[i]:
        tf_idf[word]=cal_idf[i][word]*cal_tf[i][word]
    cal_tf_idf[i]=tf_idf
cal_tf_idf 

# GET SCORE OF EACH DOCUMENT BY SUMMING THE WEIGHT OF WORDS IN A DOCUMENT
def get_score(sen):
    sentence_score=[]
    for i in cal_tf_idf :
        score=0
        for word in  cal_tf_idf[i]:
            score=score+cal_tf_idf[i][word]
        temp={'doc_id':i,'score':score,'sentence':sen[i-1]}
        sentence_score.append(temp)
    return(sentence_score) 
sentence_score=get_score(sentence)# sentence is tokenized text
print(sentence_score)
def get_summary(sentence_score):
    sum=0
    summary=[]
    array=[]
    sum=0
    for dict in sentence_score:
        """"This loop will find the avg of sentence score"""
        array.append(dict['score'])
    avg=np.sum([array])/len(sentence_score)
    std=statistics.stdev(array)# standard deviation of sentence score
    for sent in sentence_score:
        if sent['score']>avg*1.09:# +1.5*std
            summary.append(sent['sentence'])
    
    return summary
    
summary=get_summary(sentence_score)
for sent in summary:
    print(''.join(sent))
