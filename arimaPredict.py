# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 11:28:20 2017

@author: Luddite
"""

import tushare as ts
from pyramid.arima import auto_arima
import matplotlib.pyplot as plt
import datetime
import pandas as pd

class arimaPredict:
    def __init__(self,code,date):
        self.code=code;
        self.date=date;
        self.data=ts.get_hist_data(code,"2015-01-01",date);
        
    def predictor(self,days,ifCompare=False):
        fit=auto_arima(list(reversed(self.data.close.tolist())),start_p=1,max_p=9,start_q=1,max_q=6,d=1,max_d=5,seasonal=False)
        onePredict=fit.predict(n_periods=days)
        x=range(start=0,stop=days)
        y=ts.get_hist_data(self.code,start=self.date,end=str(datetime.date.today()))
        if(ifCompare):
            if(pd.nrow(y)>days):
                plt.plot(x,list(reversed(y.close.tolist()))[1:(days+1)],'g')
            else:
                plt.plot(x[0:(pd.nrow(y)-1)],list(reversed(y.close.tolist())),'g')
        plt.plot(x,onePredict,'r')
        plt.show()
    
    