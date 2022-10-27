#from sentiment_analysis import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class visualize_data:
    def __init__(self,flip,fold):
        flip=self.calc_avg(flip)
        fold=self.calc_avg(fold)
        aspects=list(flip.keys())
        flip_val=list(flip.values())
        fold_val=list(fold.values())
        
        x_axis=np.arange(len(flip_val))

        plt.bar(x_axis-0.2,flip_val,0.4,label='flip phone')
        plt.bar(x_axis+0.2,fold_val,0.4,label='fold phone')

        plt.xticks(x_axis,aspects)
        plt.xlabel('Aspects')
        plt.ylabel('sentiment values')
        plt.title('Aspect based sentiment analysis')
        plt.legend()
        plt.show()
        
    def calc_avg(self,data):
        diction=dict()
        for x in data:
            sum=0
            i=0
            for y in data[x]:
                sum+=y
                i+=1
            diction[x]=(sum/i)+1
        return diction