from nltk.corpus import stopwords
from textblob import Word
from sentiment_analysis import *
import pandas as pd
import string
string.punctuation
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
from visualize_data import *

class text_preprocessing:
    def __init__(self,web_scraping):

        self.flip_df=pd.read_csv('amazon product flip review.csv')
        self.fold_df=pd.read_csv('amazon product fold review.csv')
        
        #remove punctuations
        self.flip_df['comment']= self.flip_df['comment'].apply(lambda x:self.remove_punctuation(x))
        self.fold_df['comment']= self.fold_df['comment'].apply(lambda x:self.remove_punctuation(x))

        #lower text
        self.flip_df['comment']= self.flip_df['comment'].apply(lambda x:x.lower())
        self.fold_df['comment']= self.fold_df['comment'].apply(lambda x:x.lower())
        
        #url removes
        self.flip_df['comment'] = self.flip_df['comment'].str.replace(r'(https|http)?:\/(\w|\.|\/|\?|\=|\&|\%)*\b','')
        self.flip_df['comment'] = self.flip_df['comment'].str.replace(r'www\.\S+\.com','')
        
        #emoji 
        self.flip_df['comment'] = self.flip_df['comment'].str.replace(r'[^\x00-\x7F]+', '')
        #removes extra spaces
        self.flip_df['comment'] = self.flip_df['comment'].str.replace(r' +', ' ')

        #tokenize
        self.flip_df['comment']= self.flip_df['comment'].apply(lambda x:self.tokenization(x))
        self.fold_df['comment']= self.fold_df['comment'].apply(lambda x:self.tokenization(x))
        
        #remove stopwords
        self.stopwords=stopwords.words('english')
        self.flip_df['comment']= self.flip_df['comment'].apply(lambda x:self.remove_stopwords(x))
        self.fold_df['comment']= self.fold_df['comment'].apply(lambda x:self.remove_stopwords(x))

        #stemming
        self.porter_stemmer=PorterStemmer()
        self.flip_df['comment']= self.flip_df['comment'].apply(lambda x:self.stemming(x))
        self.fold_df['comment']= self.fold_df['comment'].apply(lambda x:self.stemming(x))
        
        #lemmatization
        self.wordnet_lemmatizer=WordNetLemmatizer()
        self.flip_df['comment']= self.flip_df['comment'].apply(lambda x:self.lemmatizer(x))
        self.fold_df['comment']= self.fold_df['comment'].apply(lambda x:self.lemmatizer(x))

        
        flip_txt=[]
        fold_txt=[]

        for x in self.flip_df['comment']:
            flip_txt+=x
        for y in self.fold_df['comment']:
            fold_txt+=y

        self.flip_analysis=sentiment_analysis(flip_txt[0])
        self.fold_analysis=sentiment_analysis(fold_txt[0])
        visualize_data(self.flip_analysis.sent_dict,self.fold_analysis.sent_dict)

        
    def lemmatizer(self,text):
        lemm_text = [self.wordnet_lemmatizer.lemmatize(word) for word in text]
        return lemm_text

    def stemming(self,text):
        stem_text = [self.porter_stemmer.stem(word) for word in text]
        return stem_text

    def tokenization(self,text):
        tokens = re.split('W+',text)
        return tokens
    
    def remove_stopwords(self,text):
        output= [i for i in text if i not in self.stopwords]
        return output

    def remove_punctuation(self,text):
        punctuationfree="".join([i for i in text if i not in string.punctuation])
        return punctuationfree
