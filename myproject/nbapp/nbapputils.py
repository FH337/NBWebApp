import pandas as pd
import string
import re
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import os
from django.conf import settings
import pickle

class Nbfunctions():
    def preprocessing(text):
        text= re.sub('\.tg.+(?=(Sumber))','',text)
        words = word_tokenize(text)
        tokens = [w for w in words if w.lower() not in string.punctuation]
        #stopw = stopwords.words('indonesian')
        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()
        tokens = [stopword.remove(token) for token in tokens]
        
        # tokens = [token for token in tokens if token not in stopw]
        # remove words less than three letters
        tokens = [word for word in tokens if len(word)>=3]
        tokens = [re.sub(r'\b\w{1,3}\b', '', token) for token in tokens]
        #tokens = re.sub(r'\b\w{1,3}\b', '', tokens)
        #remove number
        for i in range (10):
            tokens = [token.replace(str(i),'')for token in tokens]
        #lower capitalization
        tokens = [word.lower() for word in tokens]
        #stemmer
        stemmer = StemmerFactory().create_stemmer()
        tokens = [stemmer.stem(token) for token in tokens]
        # lemmatize
        #lemma = WordNetLemmatizer()
        #tokens = [lemma.lemmatize(word) for word in tokens]
        preprocessed_text = ' '.join(tokens)
        return preprocessed_text 
    
    def nbprocess(testdata, percentage):
        split = sent_tokenize(testdata)
        testpre=[]
        for i in split:
            testpre.append(Nbfunctions.preprocessing(i))
        num = 1
        wordtest = dict()
        for word in testpre:
            wordtest[num] = word_tokenize(word)
            num+=1
        df_filter=pd.read_csv("./nbapp/data/df_filter.csv")

        df_train, df_test = train_test_split(df_filter, test_size =0.25,random_state=10)
        df_0 = df_train[df_train.Label ==0]
        df_1 = df_train[df_train.Label ==1]

        df_1copy = df_1
        random.seed(6666)
        randsample = random.sample(range(df_1copy.shape[0]),df_1copy.shape[0]-df_0.shape[0])
        df_1copy=df_1copy.reset_index()
        for i in randsample:
            df_1copy=df_1copy.drop([i],axis=0)
            
        df_1copy=df_1copy.reset_index()

        PriorPOS = df_1copy["Sentence"].count()/(df_1copy["Sentence"].count()+df_0["Sentence"].count())
        PriorNEG = df_0["Sentence"].count()/(df_1copy["Sentence"].count()+df_0["Sentence"].count())
        ScorePos = PriorPOS
        ScoreNeg = PriorNEG
        
        vectorizer = CountVectorizer(ngram_range=(1,2))
        doc_vector0 = vectorizer.fit_transform(df_0['Sentence'])
        DataFrame0 = pd.DataFrame(doc_vector0.toarray().transpose(), index=vectorizer.get_feature_names())

        vectorizer = CountVectorizer(ngram_range=(1,2))
        doc_vector1 = vectorizer.fit_transform(df_1copy['Sentence'])
        DataFrame1 = pd.DataFrame(doc_vector1.toarray().transpose(), index=vectorizer.get_feature_names())

        TF0 = DataFrame0.sum(axis = 1) #TF 0
        TF0 = TF0/len(DataFrame0.columns)
        TF0 = TF0.sort_values(ascending = False)

        TF1 = DataFrame1.sum(axis = 1) #TF 1
        TF1 = TF1/len(DataFrame1.columns)
        TF1 = TF1.sort_values(ascending = False)

        df0 = DataFrame0.gt(0).sum(axis=1).sort_values(ascending=False) #Doc Freq 0
        df1 = DataFrame1.gt(0).sum(axis=1).sort_values(ascending=False) #Doc Freq 1
        
        IDF0=np.log(len(DataFrame0.columns)/DataFrame0.gt(0).sum(axis=1)) #IDF 0
        IDF1=np.log(len(DataFrame1.columns)/DataFrame1.gt(0).sum(axis=1)) #IDF 1

        TFIDF0 = TF0*IDF0
        TFIDF0 = TFIDF0.sort_values(ascending=False)
        TFIDF1 = TF1*IDF1
        TFIDF1 = TFIDF1.sort_values(ascending=False)

        Unique0 = DataFrame0.index.values.tolist()
        Unique1 = DataFrame1.index.values.tolist()
        UniqueWords = Unique0+Unique1
        UniqueWords=set(UniqueWords) #menjadikan unik list 1 dan 0

        percentTFIDF1 = TFIDF1.sort_values(ascending = False)
        percentTFIDF1 = percentTFIDF1[0:int(percentage*len(TFIDF1))]
        percentTFIDF1.to_frame()
        Vocab1=percentTFIDF1.index.values.tolist() # Mengambil vocabulary
        Corpus1 =df_1copy["Sentence"].str.cat(sep = " ")
        txt1=Corpus1.split(" ")
        txt1 = [x for x in txt1 if x!='']
        for index,i in enumerate(txt1):
            if Vocab1.count(i) == 0:
                txt1[index]=""
        txt1 = [x for x in txt1 if x!='']

        ModelPos = {}
        for i in UniqueWords:
            ModelPos[i]=((txt1.count(i))+1)/((len(txt1))+(len(UniqueWords))) #Model ( Laplace Smoothing )

        percentTFIDF0 = TFIDF0.sort_values(ascending = False)
        percentTFIDF0 = percentTFIDF0[0:int(percentage*len(TFIDF0))]
        percentTFIDF0.to_frame()
        Vocab0=percentTFIDF0.index.values.tolist() # Mengambil vocabulary
        Corpus0 =df_0["Sentence"].str.cat(sep = " ")

        txt0=Corpus0.split(" ")
        txt0 = [x for x in txt0 if x!='']
        txt0 = [x for x in txt0 if x!='-']
        for index,i in enumerate(txt0):
            if Vocab0.count(i) == 0:
                txt0[index]=""
        txt0 = [x for x in txt0 if x!='']

        
        ModelNeg = {}
        for i in UniqueWords:
            ModelNeg[i]=((txt0.count(i))+1)/((len(txt0))+(len(UniqueWords))) #Model ( Laplace Smoothing )

        ListSent = dict()
        num = 0
        for word in wordtest.values():
            for i in word:
                if i in ModelPos:
                    ScorePos+=np.log(ModelPos[i])
                else:
                    ScorePos+=np.log(1/(len(txt1)+len(UniqueWords))+1)
            for i in word:
                if i in ModelNeg:
                    ScoreNeg+=np.log(ModelNeg[i])
                else:
                    ScoreNeg+=np.log(1/(len(txt0)+len(UniqueWords))+1)
                if ScorePos > ScoreNeg:
                    ListSent[testpre[num]]="POS"
                else:
                    ListSent[testpre[num]]="NEG"
            num+=1
        
        #Df, tf, idf, tfidf, percenttfidf, prior, hasil
        return  df_0, df_1copy, df0, df1, TF0, TF1, IDF0, IDF1, TFIDF0, TFIDF1, percentTFIDF0, percentTFIDF1, PriorPOS,  PriorNEG, ListSent
