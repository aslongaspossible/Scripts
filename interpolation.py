# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:58:15 2017

@author: Luddite
"""

import tushare as ts;

class interpolation:
    def __init__(self,code,date):
        self.__code=code;
        self.__date=date;
        self.__data=ts.get_hist_data(code,"2015-01-01",date);
        
    def lagrange(self,days,ifCompare=False,daysBefore=10):
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
                        p=p*(x-j)/(k-j);
                s+=p*data[k];
            predict.append(s);
        