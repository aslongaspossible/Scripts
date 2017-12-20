# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:40:30 2017

@author: Luddite
"""
import time

class stockSimulate:
    def __init__(self,balance,fee=0.0005):
        self.balance=balance
        self.fee=fee
        self.stockList={}
        
    def buy(self,code,shares,)