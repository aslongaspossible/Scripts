# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 11:28:20 2017

@author: Luddite
"""

import tushare as ts
from pyramid.arima import auto_arima

class arimaPredict:
    def __init__(self,code,date):
        self.code=code;
        self.date=date;
        self.data=ts.get_hist_data(code,"2015-01-01",date);
        
    def predictor(self,date):
        
        
        
    
    