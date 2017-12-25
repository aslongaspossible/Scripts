# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
import tkinter.font as tkfont

class mainGUI(TK.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Price Predictor")
        self.setupGUI()
    def setupGUI(self):
        menubar=TK.Menu(self)
        filemenu=TK.Menu(menubar, tearoff=0)
        premenu=TK.Menu(menubar, tearoff=0)
        simmenu=TK.Menu(menubar, tearoff=0)
        mfont=tkfont.Font(family='Helvetica', size=15, weight=tkfont.BOLD)
        menufont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        menubar.add_cascade(label='Consultation', menu=filemenu)
        menubar.add_cascade(label='Prediction', menu=premenu)
        menubar.add_command(label='Simulation', command=self.trysimulation)
        menubar.add_command(label='About', command=self.secopyright)
        filemenu.add_command(label='History Data', accelerator='Ctrl+H', compound='left', underline=0, command=self.callthirdhistory)
        filemenu.add_separator()
        filemenu.add_command(label='Tick Data', accelerator='Ctrl+T', compound='left', underline=0, command=self.callthirdreal)
        premenu.add_command(label='Arima Self-correlation', accelerator='Ctrl+A', compound='left', underline=0, command=self.callthirdhistory)
        premenu.add_separator()
        premenu.add_command(label='Lagrange Interpolation', accelerator='Ctrl+L', compound='left', underline=0, command=self.callthirdreal)
        self.config(menu=menubar)
        
        #构建主界面上的上证指数和
        thirdf=TK.Frame(self, borderwidth=4, pady=30, bg='white')
        thirdf.pack(side=TK.LEFT)
        labeltitle=TK.Label(thirdf, text="Shangzheng Index Information", font=mfont, bg='white')
        labeltitle.pack(side=TK.TOP, fill=TK.BOTH)
        shangzhenghis=historyData('sh', str(dt.date.today()-dt.timedelta(days=90)), str(dt.date.today()))
        shangzhenghis.plotCandleStick(ma5=True,ma10=True,ma20=True,volume=True)
        self.dpimg = ImageTk.PhotoImage(file='sh'+'_'+str(dt.date.today()-dt.timedelta(days=90))+'_'+str(dt.date.today())+'.png')
        TK.Label(thirdf, image=self.dpimg).pack(side=TK.TOP)
        TK.Label(thirdf, text='By 理科小矿工', font=menufont, bg='white').pack(side=TK.TOP)
    def callthirdhistory(self):
        thirdhistory=thilayerhistory() 
    def callthirdreal(self):
        thirdreal=thilayerrealtime()
    def secopyright(self):
        thirdcopy=showcopyright()
    def trysimulation(self):
        thirdsim=seclayersim()
        
class showcopyright(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Copyright')
        self.geometry('400x100')
        self.resizable(width=False, height=False)
        menufont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        TK.Label(self, text='Copyright Reserved to 理科小矿工 丁思凡，颜峻',font=menufont, pady=30).pack()
        
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
        row_bal4=TK.Frame(self)
        row_bal4.pack(side=TK.TOP, fill=TK.X)
        startdate=TK.Label(row_bal4, text='Start Date',width=10)
        startdate.pack(side=TK.LEFT)
        self.sdate=TK.StringVar()
        Date_entry=TK.Entry(row_bal4, textvariable=self.sdate,width=10)
        Date_entry.pack(side=TK.LEFT)
        TK.Button(row_bal3, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row_bal3, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
    def Confirm(self):
        sts=ss.stockSimulate(self.balance.get(), self.sdate.get())
        thirdsim=thilayersimulate()
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
        
if __name__=='__main__':
    haha=mainGUI()
    haha.mainloop()
        