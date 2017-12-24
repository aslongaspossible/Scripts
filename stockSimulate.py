# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:40:30 2017

@author: Luddite
"""
#import pandas as pd
import tushare as ts
import time

class stockSimulate:
    def __init__(self,balance,startDate,startTime='00:00:00',fee=0.0005,tax=0.001):
        self.__balance=float(balance)
        self.__fee=float(fee)
        self.__tax=float(tax)
        self.__time=startTime
        self.__date=startDate
        self.__stockList={}
        self.__earlyStartTime=self.__timeToStamp('09:30:00')
        self.__earlyEndTime=self.__timeToStamp('11:30:00')
        self.__afterStartTime=self.__timeToStamp('13:00:00')
        self.__afterEndTime=self.__timeToStamp('15:00:00')
        
        
    def __timeToStamp(inputTime,inputDate='2017-12-19'):
        c=time.mktime(time.strptime(inputDate+' '+inputTime,"%Y-%m-%d %H:%M:%S"))
        return c
        
    def __matchTime(self,data,matchTime):
        hitIndexes=data[data.time==matchTime].index.tolist()
        
        if(len(hitIndexes)>0):
            hitIndex=hitIndexes[0]
        else:
            floatT=self.__timeToStamp(matchTime)
            times=data.time.map(self.__timeToStamp)
            indexMax=data.index.max()
            indexMin=0
            hitIndex=indexMax/2
            while(indexMax>indexMin):
                if(times[hitIndex]>floatT):
                    indexMin=hitIndex+1
                else:
                    indexMax=hitIndex
                hitIndex=(indexMin+indexMax)/2
        
        return hitIndex
    
    def __isTradeTime(self,time):
        floatT=self.__timeToStamp(time)
        isTradingTime=True
        if(floatT<self.__earlyStartTime or floatT>self.__afterEndTime):
            isTradingTime=False
        if(floatT>self.__earlyEndTime and floatT<self.__afterStartTime):
            isTradingTime=False
        return isTradingTime
        
    def __tradeCommission(self,volumes):
        commission=volumes*self.__fee
        if(commission<5):
            commission=5
        
        return commission
            
    
    def buy(self,code,shares,buyDate,buyTime):
        if(self.__timeToStamp(buyTime,buyDate)<self.__timeToStamp(self.__time,self.__date)):
            print('invalid time')
        else:
            buyDayData=ts.get_tick_data(code,buyDate)
            if(buyDayData.price[0]!=buyDayData.price[0]):
                print('not a TRADING DAY')
            elif(not self.__isTradeTime(buyTime)):
                print('not in trading time')
            else:
                hitIndex=self.__matchTime(buyDayData,buyTime)
                buyPrice=buyDayData.price[hitIndex].tolist()[0]
                
                commission=(buyPrice*float(shares))
                
                newBalance=self.__balance-buyPrice*float(shares)-commission
                if(newBalance<0):
                    print('balance not enough!')
                else:
                    if(self.__stockList.has_key(code)):
                        self.__stockList[code]+=shares
                    else:
                        self.__stockList[code]=shares
                    self.__balance=newBalance
                    
    def showAccount(self):
        print('balance:'+self.__balance)
        for code in self.__stockList.keys():
            print(code+':'+self.__stockList[code])
        
    def sell(self,code,shares,sellDate,sellTime):
        if(self.__timeToStamp(sellTime,sellDate)<self.__timeToStamp(self.__time,self.__date)):
            print('invalid time')
        else:
            if(not self.__stockList.has_key[code]):
                print('not have this stock')
            else:
                newShares=self.__stockList[code]-shares
                if(newShares<0):
                    print('shares not enough')
                else:
                    sellDayData=ts.get_tick_data(code,sellDate)
                    
                if(sellDayData.price[0]!=sellDayData.price[0]):
                    print('not a TRADING DAY')
                elif(not self.__isTradeTime(sellTime)):
                    print('not in trading time')
                else:
                    hitIndex=self.__matchTime(sellDayData,sellTime)
                    sellPrice=sellDayData.price[hitIndex].tolist()[0]
                    commission=self.__tradeCommission(sellPrice*float(shares))
                    newBalance=self.__balance+sellPrice*float(shares)*(1-self.__tax)-commission
                    if(newBalance<0):
                        print('balance not enough!')
                    else:
                        self.__balance=newBalance
                        self.__stockList[code]=newShares
                