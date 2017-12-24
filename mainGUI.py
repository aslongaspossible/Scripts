#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 08:25:14 2017

@author: bwlab
"""
import tkinter as TK
from PIL import Image, ImageTk
import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
from matplotlib.finance import candlestick_ohlc
import datetime as dt
import stockSimulate as ss
from arimaPredict import *
from historyData import *
from tickData import *
                
class figureplot(TK.Toplevel):  #单独构造画图类
    def __init__(self, plotinfo):
        super().__init__()
        self.title("Stock Price Viewer")
        #figplot=TK.Frame(self)
        #figplot.pack(side=TK.TOP, fill=TK.X)
        self.img = ImageTk.PhotoImage(file=plotinfo)
        TK.Label(self, image=self.img).pack(side=TK.TOP)        
        
class seclayercon(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("See Stock Price")
        seclayercon_fir=TK.Frame(self)
        seclayercon_fir.pack(side=TK.TOP)
        seclayercon_title=TK.Label(seclayercon_fir, text="Please Select")
        seclayercon_title.pack(side=TK.LEFT, fill=TK.BOTH)
        seclayercon_sec=TK.Frame(self)
        seclayercon_sec.pack(side=TK.TOP)
        TK.Button(seclayercon_sec, text="Period Data", width=30, height=3, command=self.callthirdhistory).pack(side=TK.TOP, fill=TK.X)
        TK.Button(seclayercon_sec, text="Day Data", width=30, height=3, command=self.callthirdreal).pack(side=TK.TOP, fill=TK.X)
    def callthirdhistory(self):
        thirdhistory=thilayerhistory()
    def callthirdreal(self):
        thirdreal=thilayerrealtime()
        
class seclayerpre(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Predict Stock Price")
        row_1=TK.Frame(self)
        row_1.pack(side=TK.TOP, fill=TK.X)
        stock_code1=TK.Label(row_1, text='Stock Code',width=10)
        stock_code1.pack(side=TK.LEFT)
        self.stockcode1=TK.StringVar()
        codeentry=TK.Entry(row_1, textvariable=self.stockcode1,width=35)
        codeentry.pack(side=TK.LEFT)
        row_explain=TK.Frame(self)
        row_explain.pack(side=TK.TOP,fill=TK.X)
        row_3=TK.Frame(self)
        row_3.pack(side=TK.TOP, fill=TK.X)
        PDL=TK.Label(row_3, text='End Date', width=10)
        PDL.pack(side=TK.LEFT)
        self.enddate=TK.StringVar()
        edp=TK.Entry(row_3, textvariable=self.enddate, width=35)
        edp.pack(side=TK.LEFT)
        row_explain=TK.Frame(self)
        row_explain.pack(side=TK.TOP)
        TK.Label(row_explain, text='End Date Means the end date for prediction parameter setup').pack(side=TK.LEFT)
        row_5=TK.Frame(self, pady=10)
        row_5.pack(side=TK.TOP)
        pdays=TK.Label(row_5, text='Prediction Days', width=15)
        pdays.pack(side=TK.LEFT)
        self.predays=TK.IntVar()
        pd=TK.Entry(row_5, textvariable=self.predays, width=30)
        pd.pack(side=TK.LEFT)
        #TK.Label(row_explain, text='setup and the starting date is 2015-01-01').pack(side=TK.TOP)
        #TK.Label(row_explain, text='请输入yyyy-mm-dd,如2017-01-01').pack(side=TK.TOP)
        #row_2=TK.Frame(self)
        #row_2.pack(side=TK.TOP,fill=TK.X)
        #self.var=TK.IntVar()
        #self.var.set(1)
        #TK.Radiobutton(row_2, text='Method 1', value=1, variable=self.var).pack(side=TK.LEFT)
        #TK.Radiobutton(row_2, text='Method 2', value=2, variable=self.var).pack(side=TK.LEFT)
        #TK.Radiobutton(row_2, text='Method 3', value=3, variable=self.var).pack(side=TK.LEFT)
        #TK.Radiobutton(row_2, text='Method 4', value=4, variable=self.var).pack(side=TK.LEFT)        
        row4=TK.Frame(self)               #选项确定和取消  
        row4.pack(side=TK.TOP, fill=TK.X)
        TK.Button(row4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
    def Confirm(self):
        print('this is a test')
        #a=arimaPredict(self.stockcode1.get(),self.enddate.get())
        #a.predictor(self.predays.get())
    def Cancel(self):
        self.destroy()
#class seclayersug(TK.Toplevel):
        
class seclayersim(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Stock Price Simulator")
        row_bal3=TK.Frame(self)
        row_bal3.pack(side=TK.TOP, fill=TK.X)
        stock_code3=TK.Label(row_bal3, text='Balance',width=10)
        stock_code3.pack(side=TK.LEFT)
        self.balance=TK.IntVar()
        balance_entry=TK.Entry(row_bal3, textvariable=self.balance,width=10)
        balance_entry.pack(side=TK.LEFT)
        TK.Button(row_bal3, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row_bal3, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
    def Confirm(self):
        sts=ss.stockSimulate(self.balance.get())
        thirdsim=thilayersimulate()
        print("haha")
    def Cancel(self):
        self.destroy()
        
class thilayersimulate(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Stock Price Simulator")
        row_bal=TK.Frame(self)
        row_bal.pack(side=TK.TOP, fill=TK.X)
        stock_code2=TK.Label(row_bal, text='Stock Code',width=10)
        stock_code2.pack(side=TK.LEFT)
        self.stockcode2=TK.StringVar()
        code_entry=TK.Entry(row_bal, textvariable=self.stockcode2,width=33)
        code_entry.pack(side=TK.LEFT)
        row_sim1=TK.Frame(self)
        row_sim1.pack(side=TK.TOP, fill=TK.X)
        row_sim2=TK.Frame(self)
        row_sim2.pack(side=TK.TOP, fill=TK.X)
        self.var=TK.IntVar()
        self.var.set(1)
        TK.Radiobutton(row_sim1, text='Execute Buy', value=1, variable=self.var).pack(side=TK.LEFT)
        TK.Radiobutton(row_sim2, text='Execute Sell', value=2, variable=self.var).pack(side=TK.LEFT)
        share=TK.Label(row_sim1, text='Share Amount',width=15)
        share.pack(side=TK.LEFT)      
        self.shareamount=TK.IntVar()
        share_entry=TK.Entry(row_sim1, textvariable=self.shareamount,width=17)
        share_entry.pack(side=TK.LEFT)
        Dateop=TK.Label(row_sim2, text="     Date", width=5)
        Dateop.pack(side=TK.LEFT)
        self.opdate=TK.IntVar()
        Date_entry=TK.Entry(row_sim2, textvariable=self.opdate,width=10)
        Date_entry.pack(side=TK.LEFT)
        Timeop=TK.Label(row_sim2, text="Time", width=5)
        Timeop.pack(side=TK.LEFT)
        self.optime=TK.IntVar()
        Time_entry=TK.Entry(row_sim2, textvariable=self.optime,width=10)
        Time_entry.pack(side=TK.LEFT)
        row_sim3=TK.Frame(self)
        row_sim3.pack(side=TK.TOP, fill=TK.X)
        TK.Button(row_sim3, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row_sim3, text='Execute', width=6, command=self.Execute).pack(side=TK.RIGHT) #self.drawfigure())
        TK.Button(row_sim3, text='Show Account', width=10, command=self.showaccount).pack(side=TK.RIGHT)
    def Cancel(self):
        self.destroy()
    def Execute(self):
        self.opcode=self.stockcode2.get()
        self.opshare=self.shareamount.get()
        self.operationdate=self.opdate.get()
        #if(var.get()==1):
        #    simulate.buy
    def showaccount(self):
        print("this is not complete")
                
class thilayerhistory(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("See Period Data")
        row1=TK.Frame(self)               #股票代码
        row1.pack(side=TK.TOP, fill=TK.X)    
        stock_code=TK.Label(row1, text='Stock Code',width=10)
        stock_code.pack(side=TK.LEFT)
        self.stockcode=TK.StringVar()
        codeentry=TK.Entry(row1, textvariable=self.stockcode,width=30)
        codeentry.pack(side=TK.LEFT)
        row2=TK.Frame(self)             #查询时间
        row2.pack(side=TK.TOP, fill=TK.X)   
        start_time=TK.Label(row2, text='Start Date', width=10)
        start_time.pack(side=TK.LEFT)
        self.starttime=TK.StringVar()
        starttimeentry=TK.Entry(row2,textvariable=self.starttime, width=10)
        starttimeentry.pack(side=TK.LEFT)
        end_time=TK.Label(row2, text='End Date', width=10)
        end_time.pack(side=TK.LEFT)
        self.endtime=TK.StringVar()
        endtimeentry=TK.Entry(row2,textvariable=self.endtime, width=10)
        endtimeentry.pack(side=TK.LEFT)        
        row3=TK.Frame(self)                
        row3.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(row3, text='         (请输入yyyy-mm-dd,如2017-01-01)')
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
        row4=TK.Frame(self)               #选项确定和取消  
        row4.pack(side=TK.TOP, fill=TK.X)
        TK.Button(row4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
    def Confirm(self):
        self.code=self.stockcode.get()
        self.stdate=self.starttime.get()
        self.endate=self.endtime.get()
        drawhistory=historyData(self.code, self.stdate, self.endate)
        drawhistory.plotCandleStick()
        self.plotinfo1=self.code+'_'+self.stdate+'_'+self.endate+'.png'
        hisgraph=figureplot(self.plotinfo1)    
    def Cancel(self):
        self.destroy()
        
class thilayerrealtime(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("See Day Data")
        row1=TK.Frame(self)               #股票代码
        row1.pack(side=TK.TOP, fill=TK.X)    
        stock_code=TK.Label(row1, text='Stock Code',width=10)
        stock_code.pack(side=TK.LEFT)
        self.stockcode2=TK.StringVar()
        codeentry=TK.Entry(row1, textvariable=self.stockcode2,width=30)
        codeentry.pack(side=TK.LEFT)  
        row2=TK.Frame(self)             #查询时间
        row2.pack(side=TK.TOP, fill=TK.X)   
        start_time=TK.Label(row2, text='Date', width=10)
        start_time.pack(side=TK.LEFT)
        self.starttime2=TK.StringVar()
        starttimeentry=TK.Entry(row2,textvariable=self.starttime2, width=10)
        starttimeentry.pack(side=TK.LEFT)
        row4=TK.Frame(self)               #选项确定和取消  
        row4.pack(side=TK.TOP, fill=TK.X)
        TK.Button(row4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
    def Confirm(self):       
        self.code2=self.stockcode2.get()
        self.stdate2=self.starttime2.get()
        detail=tickData(self.code2, self.stdate2)
        detail.plotTickLine()
        self.plotinfo2=self.code2+'_'+self.stdate2+'.png'
        detgraph=figureplot(self.plotinfo2)
    def Cancel(self):
        self.destroy()       

class mainGUI(TK.Tk):
    def __init__(self):
        super().__init__()
        self.title("stock price assistance")
        self.setupGUI()
    def setupGUI(self):
        firstf=TK.Frame(self)
        firstf.pack(side=TK.TOP)
        labeltitle=TK.Label(firstf, text="Please Select")
        labeltitle.pack(side=TK.LEFT, fill=TK.BOTH)
        secondf=TK.Frame(self,  relief=TK.GROOVE, borderwidth=2)
        secondf.pack(side=TK.TOP)
        TK.Button(secondf, text="Consultation", width=16, height=2,  command=self.conwin).pack(side=TK.LEFT)
        TK.Button(secondf, text="Prediction", width=16, height=2,  command=self.prewin).pack(side=TK.LEFT)
        TK.Button(secondf, text="Simulation", width=16, height=2,  command=self.sugwin).pack(side=TK.LEFT)
        thirdf=TK.Frame(self, relief=TK.RAISED, borderwidth=4, pady=30)
        thirdf.pack(side=TK.LEFT)
        labeltitle=TK.Label(thirdf, text="History Shangzheng Index Information")
        labeltitle.pack(side=TK.TOP, fill=TK.BOTH)
        shangzhenghis=historyData('sh', str(dt.date.today()-dt.timedelta(days=90)), str(dt.date.today()))
        self.dpimg = ImageTk.PhotoImage(file='sh'+'_'+str(dt.date.today()-dt.timedelta(days=90))+'_'+str(dt.date.today())+'.png')
        TK.Label(thirdf, image=self.dpimg).pack(side=TK.TOP)
        #fourthf=TK.Frame(self, relief=TK.RAISED, borderwidth=4, pady=30)
        #fourthf.pack(side=TK.LEFT)
        #labeltitle=TK.Label(fourthf, text="Realtime Shangzheng Index Information")
        #labeltitle.pack(side=TK.TOP, fill=TK.BOTH)
        #shangzhengreal=tickData('000001',str(dt.date.today()))
        #self.rlimg = ImageTk.PhotoImage(file='000001'+'_'+str(dt.date.today())+'.png')
        #TK.Label(fourthf, image=self.rlimg).pack(side=TK.TOP)
    def conwin(self):
        secconwin=seclayercon()
    def prewin(self):
        secprewin=seclayerpre()
    def sugwin(self):
        secsimulate=seclayersim()

if __name__=='__main__':
    haha=mainGUI()
    haha.mainloop()
    