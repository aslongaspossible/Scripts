# -*- coding: utf-8 -*-
"""
Created on Thu Dec 07 15:27:00 2017

@author: 丁思凡
"""

import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
from matplotlib.finance import candlestick_ohlc

class historyData:    
    def __init__(self,code,startTime,endTime):
        self.code=code;
        self.start=startTime;
        self.end=endTime;
        self.data=ts.get_hist_data(code,start=startTime,end=endTime);
        self.ohlc = zip(self.data.index.map(self.stringToFloatDate),self.data.open,self.data.high,self.data.low,self.data.close)
     
    def stringToFloatDate(self,myString):
        myDate=datetime.strptime(myString, '%Y-%m-%d');
        return dates.date2num(myDate);
     
    def plotCandleStick(self,height=7,width=10,ma5=False,ma10=False,ma20=False,volume=False):
        times=self.data.index.map(self.stringToFloatDate)
        if(volume):
            fig,(ax,ax2)=plt.subplots(nrows=2,sharex='col',gridspec_kw = {'height_ratios':[2, 1]})
            ax2.bar(times,self.data.volume)
        else:
            fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        fig.set_figheight(height)
        fig.set_figwidth(width)
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        if(ma5):
            ax.plot(times,self.data.ma5)
        if(ma10):
            ax.plot(times,self.data.ma10)
        if(ma20):
            ax.plot(times,self.data.ma20)
        candlestick_ohlc(ax,self.ohlc,width =0.4,colorup='r',colordown='g')
        fig.savefig(self.code+'_'+self.start+'_'+self.end+'.png')
        
    def plotCloseLine(self,height=7,width=10):
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        fig.set_figheight(height)
        fig.set_figwidth(width)
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.plot(self.data.index.map(self.stringToFloatDate), self.data.close)
        fig.savefig(self.code+'_'+self.start+'_'+self.end+'.png')
        