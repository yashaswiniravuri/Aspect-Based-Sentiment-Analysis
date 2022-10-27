import spacy
from gensim.models import *
from sklearn.metrics.pairwise import cosine_similarity
from text_preprocessing import *
from visualize_data import *
#https://www.kaggle.com/datasets/sandreds/googlenewsvectorsnegative300
class sentiment_analysis:
    def __init__(self,data):
        self.data = spacy.load("en_core_web_sm")(data)
        file = open('positive-words.txt', 'r')
        pos= file.read().split()
        file = open('negative-words.txt', 'r')
        neg= file.read().split()
        self.wv = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
        self.aspects=['performance','money','screen','camera','speed']
        self.aspects_vectors=[self.wv['performance'],self.wv['money'],self.wv['screen'],self.wv['camera'],self.wv['speed']]
        self.sent_dict={'performance':[0],'money':[0],'screen':[0],'camera':[0],'speed':[0]}
        self.feature_sentiment(self.data, pos, neg)
        print(self.sent_dict)

    def add(self,word,sentiment):
        sim=[]
        for i in range(0,5):
            try:
                sim.append(cosine_similarity([self.wv[word]],[self.aspects_vectors[i]]))
            except Exception as e:
                sim.append(0)
        max=0
        curr=0
        for i in range(0,5):
            if(sim[i]>max):
                max=sim[i]
                curr=i
        if max!=0:
            self.sent_dict[self.aspects[curr]].append(sentiment)

    def feature_sentiment(self,sentence, pos, neg):
        opinion_words = neg + pos
        debug = 0
        for token in sentence:
            if token.text in opinion_words:
                sentiment = 1 if token.text in pos else -1
                if (token.dep_ == "advmod"):
                    continue
                elif (token.dep_ == "amod"):
                    self.add(token.head.text,sentiment)
                else:
                    for child in token.children:
                        if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in opinion_words):
                            sentiment *= 1.5
                        if child.dep_ == "neg":
                            sentiment *= -1
                    for child in token.children:
                        if (token.pos_ == "VERB") & (child.dep_ == "dobj"):                        
                            self.add(child.text, sentiment)
                            subchildren = []
                            conj = 0
                            for subchild in child.children:
                                if subchild.text == "and":
                                    conj=1
                                if (conj == 1) and (subchild.text != "and"):
                                    subchildren.append(subchild.text)
                                    conj = 0
                            for subchild in subchildren:
                                self.add(subchild,sentiment)
                    for child in token.head.children:
                        noun = ""
                        if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in opinion_words):
                            sentiment *= 1.5
                        if (child.dep_ == "neg"): 
                            sentiment *= -1
                    for child in token.head.children:
                        noun = ""
                        if (child.pos_ == "NOUN"):
                            noun = child.text
                        debug += 1