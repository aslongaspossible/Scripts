# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:58:15 2017

@author: Luddite
"""

import tushare as ts
import matplotlib.pyplot as plt
import datetime

class interpolation:
    def __init__(self,code,date):
        self.__code=code;
        self.__date=date;
        self.__data=ts.get_hist_data(code,"2015-01-01",date);
        self.__length=len(self.__data.index.tolist());
        
    def lagrange(self,days=3,ifCompare=False,daysBefore=4):
        if(self.__length<daysBefore):
            daysBefore=self.__length;
        data=list(reversed(self.__data.close[0:daysBefore].tolist()));
        predict=[];
        x=range(days);
        xBefore=range(-daysBefore,0);
        for i in x:
            s=0.0;
            for k in xBefore:
                p=1.0;
                for j in xBefore:
                    if(j!=k):
                        p=p*(i-j)/(k-j);
                s+=p*data[k];
            predict.append(s);
        #print(predict);
        fig, ax = plt.subplots();
        if(ifCompare):
            futureData=ts.get_hist_data(self.__code,start=self.__date,end=str(datetime.date.today()));
            futureClose=list(reversed(futureData.close.tolist()))[1:];
            if(len(futureClose)<days):
                ax.plot(x[0:len(futureClose)],futureClose,'g',label='real');
            else:
                ax.plot(x,futureClose[:days],'g',label='real');
            #print(futureClose);
        ax.plot(x,predict,'r',label='predict');
        ax.legend();
        fig.savefig('lagrange_'+self.__code+'_'+self.__date+'_'+str(days)+'.png');