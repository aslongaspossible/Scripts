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
from datetime import date
from matplotlib import dates
from matplotlib.finance import candlestick_ohlc
import datetime as dt
import stockSimulate as ss
from stockPredict import *
from historyData import *
from tickData import *
import tkinter.font as tkfont

class figureplot(TK.Toplevel):  #单独构造画图类
    def __init__(self, plotinfo, stockcode):
        super().__init__()
        self.title("Stock Price Viewer")
        self.resizable(width=False, height=False)
        tfont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        plottitle=TK.Frame(self)
        plottitle.pack()
        plotlabel=TK.Label(plottitle,text='Stock'+'  '+stockcode,font=tfont)
        plotlabel.pack(pady=5)
        #figplot=TK.Frame(self)
        #figplot.pack(side=TK.TOP, fill=TK.X)
        self.img = ImageTk.PhotoImage(file=plotinfo)
        TK.Label(self, image=self.img).pack(side=TK.TOP) 
    
class mainGUI(TK.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Price Predictor")
        self.setupGUI()
        self.resizable(width=False, height=False)
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
        premenu.add_command(label='Arima Self-correlation', accelerator='Ctrl+A', compound='left', underline=0, command=self.callarima)
        premenu.add_separator()
        premenu.add_command(label='Lagrange Interpolation', accelerator='Ctrl+L', compound='left', underline=0, command=self.calllag)
        self.config(menu=menubar)
        
        #构建主界面上的上证指数和
        thirdf=TK.Frame(self, borderwidth=4, pady=20, bg='white')
        thirdf.pack(side=TK.LEFT)
        labeltitle=TK.Label(thirdf, text="Shangzheng Index Information", font=mfont, bg='white')
        labeltitle.pack(side=TK.TOP, fill=TK.BOTH)
        shangzhenghis=historyData('sh', str(dt.date.today()-dt.timedelta(days=90)), str(dt.date.today()))
        shangzhenghis.plotCandleStick(ma5=True,ma10=True,ma20=True,volume=True)
        self.dpimg = ImageTk.PhotoImage(file='sh'+'_'+str(dt.date.today()-dt.timedelta(days=90))+'_'+str(dt.date.today())+'.png')
        TK.Label(thirdf, image=self.dpimg).pack(side=TK.TOP)
    def callthirdhistory(self):
        thirdhistory=thilayerhistory() 
    def callthirdreal(self):
        thirdreal=thilayerrealtime()
    def callarima(self):
        secarima=seclayerarima()
    def calllag(self):
        seclag=seclayerlt()
    def secopyright(self):
        thirdcopy=showcopyright()
    def trysimulation(self):
        thirdsim=seclayersim()
        
class seclayerarima(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('ARIMA Prediction')
        self.resizable(width=False, height=False)
        arifont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        arimamain=TK.Frame(self, relief=TK.GROOVE, borderwidth=2)
        arimamain.pack(side=TK.TOP, fill=TK.X)
        TK.Label(arimamain, text='Please Enter the following information', font=arifont).pack(side=TK.TOP)
        arima2=TK.Frame(arimamain)               #股票代码
        arima2.pack(side=TK.TOP, fill=TK.X)    
        arima_code=TK.Label(arima2, text='Stock Code',width=10)
        arima_code.pack(side=TK.LEFT)
        self.arimacode=TK.StringVar()
        arimaentry1=TK.Entry(arima2, textvariable=self.arimacode,width=10)
        arimaentry1.pack(side=TK.LEFT)
        #arima3=TK.Frame(self)             #查询时间
        #arima3.pack(side=TK.TOP, fill=TK.X)   
        arimastart=TK.Label(arima2, text='Start Date', width=10)
        arimastart.pack(side=TK.LEFT)
        self.arimatime=TK.StringVar()
        arimatimeentry=TK.Entry(arima2,textvariable=self.arimatime, width=10)
        arimatimeentry.pack(side=TK.LEFT)
        arimaend=TK.Label(arima2, text='Prediction Days', width=15)
        arimaend.pack(side=TK.LEFT)
        self.arima_days=TK.IntVar()
        dayentry=TK.Entry(arima2,textvariable=self.arima_days, width=10)
        dayentry.pack(side=TK.LEFT)        
        arima4=TK.Frame(arimamain)               #选项确定和取消  
        arima4.pack(side=TK.TOP, fill=TK.X, pady=10)
        TK.Button(arima4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(arima4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
        noteframe=TK.Frame(self, relief=TK.GROOVE, borderwidth=2)
        noteframe.pack(side=TK.TOP, fill=TK.X)
        arima1=TK.Frame(noteframe)                
        arima1.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(arima1, text='Stock code such as 600292, Date format is yyyy-mm-dd, such as 2017-01-01')
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
        supframe=TK.Frame(noteframe)
        supframe.pack(side=TK.TOP, fill=TK.X)
        TK.Label(supframe, text='Arima Prediction is based on the self-correlation of stockprice').pack(side=TK.LEFT)
        
    def Confirm(self):
        confirmcode=self.arimacode.get()
        confirmtime=self.arimatime.get()
        confirmday=self.arima_days.get()
        myarima=stockPredict(confirmcode, confirmtime)
        myarima.arimaPredictor(confirmday)
        self.plotarima='arima_'+confirmcode+'_'+confirmtime+'_'+str(confirmday)+'.png'
        arimagraph=figureplot(self.plotarima, confirmcode+'  ARIMA'+'_'+confirmtime+'_'+str(confirmday)+' days')
    def Cancel(self):
        self.destroy()
        
class seclayerlt(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Lagrange Interpolation Prediction')
        self.resizable(width=False, height=False)
        ltfont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        ltmain=TK.Frame(self, relief=TK.GROOVE, borderwidth=2)
        ltmain.pack(side=TK.TOP, fill=TK.X)
        TK.Label(ltmain, text='Please Enter the following information', font=ltfont).pack(side=TK.TOP)
        lt2=TK.Frame(ltmain)               #股票代码
        lt2.pack(side=TK.TOP, fill=TK.X)    
        lt_code=TK.Label(lt2, text='Stock Code',width=10)
        lt_code.pack(side=TK.LEFT)
        self.ltcode=TK.StringVar()
        ltentry1=TK.Entry(lt2, textvariable=self.ltcode,width=10)
        ltentry1.pack(side=TK.LEFT)
        #arima3=TK.Frame(self)             #查询时间
        #arima3.pack(side=TK.TOP, fill=TK.X)   
        ltstart=TK.Label(lt2, text='Start Date', width=10)
        ltstart.pack(side=TK.LEFT)
        self.lttime=TK.StringVar()
        lttimeentry=TK.Entry(lt2,textvariable=self.lttime, width=10)
        lttimeentry.pack(side=TK.LEFT)
        ltend=TK.Label(lt2, text='Prediction Days', width=15)
        ltend.pack(side=TK.LEFT)
        self.lt_days=TK.IntVar()
        ltdayentry=TK.Entry(lt2,textvariable=self.lt_days, width=10)
        ltdayentry.pack(side=TK.LEFT)        
        lt4=TK.Frame(ltmain)               #选项确定和取消  
        lt4.pack(side=TK.TOP, fill=TK.X, pady=10)
        TK.Button(lt4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(lt4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
        ltnoteframe=TK.Frame(self, relief=TK.GROOVE, borderwidth=2)
        ltnoteframe.pack(side=TK.TOP, fill=TK.X)
        lt1=TK.Frame(ltnoteframe)                
        lt1.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(lt1, text='Stock code such as 600292, Date format is yyyy-mm-dd, such as 2017-01-01')
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
        ltsupframe=TK.Frame(ltnoteframe)
        ltsupframe.pack(side=TK.TOP, fill=TK.X)
        TK.Label(ltsupframe, text='Lagrange Interpolation is a numeric method').pack(side=TK.LEFT)
        
    def Confirm(self):
        ltconfirmcode=self.ltcode.get()
        ltconfirmtime=self.lttime.get()
        ltconfirmday=self.lt_days.get()
        mylt=stockPredict(ltconfirmcode, ltconfirmtime)
        mylt.lagrangeInterpolation(ltconfirmday)
        self.plotlt='lagrange_'+ltconfirmcode+'_'+ltconfirmtime+'_'+str(ltconfirmday)+'.png'
        ltgraph=figureplot(self.plotlt, ltconfirmcode+'  lagrange'+'_'+ltconfirmtime+'_'+str(ltconfirmday)+' days')
    def Cancel(self):
        self.destroy()
        
        
class showcopyright(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Copyright')
        self.geometry('400x100')
        self.resizable(width=False, height=False)
        menufont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        TK.Label(self, text='Copyright Reserved to 理科小矿工 丁思凡，颜峻',font=menufont, pady=20).pack()
        
class thilayerhistory(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("See Period Data")
        self.resizable(width=False, height=False)
        hisfont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        row_main=TK.Frame(self, relief=TK.GROOVE, borderwidth=2)
        row_main.pack(side=TK.TOP, fill=TK.X)
        TK.Label(row_main, text='Please Enter the following information', font=hisfont, pady=5).pack(side=TK.TOP)
        row1=TK.Frame(row_main,pady=5)               #股票代码
        row1.pack(side=TK.TOP, fill=TK.X)    
        stock_code=TK.Label(row1, text='Stock Code',width=10)
        stock_code.pack(side=TK.LEFT)
        self.stockcode=TK.StringVar()
        codeentry=TK.Entry(row1, textvariable=self.stockcode,width=35)
        codeentry.pack(side=TK.LEFT)
        row2=TK.Frame(row_main)             #查询时间
        row2.pack(side=TK.TOP, fill=TK.X)   
        start_time=TK.Label(row2, text='Start Date', width=10)
        start_time.pack(side=TK.LEFT)
        self.starttime=TK.StringVar()
        starttimeentry=TK.Entry(row2,textvariable=self.starttime, width=12)
        starttimeentry.pack(side=TK.LEFT)
        end_time=TK.Label(row2, text='End Date', width=10)
        end_time.pack(side=TK.LEFT)
        self.endtime=TK.StringVar()
        endtimeentry=TK.Entry(row2,textvariable=self.endtime, width=12)
        endtimeentry.pack(side=TK.LEFT)        
        row4=TK.Frame(row_main)               #选项确定和取消  
        row4.pack(side=TK.TOP, fill=TK.X, pady=15)
        TK.Button(row4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
        row3=TK.Frame(self, relief=TK.GROOVE, borderwidth=2, pady=5)                
        row3.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(row3, text='Stock code such as 600292, Date format is yyyy-mm-dd')
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
    def Confirm(self):
        self.code=self.stockcode.get()
        self.stdate=self.starttime.get()
        self.endate=self.endtime.get()
        drawhistory=historyData(self.code, self.stdate, self.endate)
        drawhistory.plotCandleStick(ma5=True,ma10=True,ma20=True,volume=True)
        self.plotinfo1=self.code+'_'+self.stdate+'_'+self.endate+'.png'
        hisgraph=figureplot(self.plotinfo1, self.code)    
    def Cancel(self):
        self.destroy()
        
class thilayerrealtime(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("See Tick Data")
        self.resizable(width=False, height=False)
        tickfont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        row_main=TK.Frame(self, relief=TK.GROOVE, borderwidth=2)
        row_main.pack(side=TK.TOP, fill=TK.X)
        TK.Label(row_main, text='Please Enter the following information', font=tickfont, pady=5).pack(side=TK.TOP)
        rowl=TK.Frame(row_main)                
        rowl.pack(side=TK.TOP, fill=TK.X)
        stock_code=TK.Label(rowl, text='Stock Code',width=10)
        stock_code.pack(side=TK.LEFT)
        self.stockcode2=TK.StringVar()
        codeentry=TK.Entry(rowl, textvariable=self.stockcode2,width=15)
        codeentry.pack(side=TK.LEFT)     
        start_time=TK.Label(rowl, text='Date', width=10)
        start_time.pack(side=TK.LEFT)
        self.starttime2=TK.StringVar()
        starttimeentry=TK.Entry(rowl,textvariable=self.starttime2, width=10)
        starttimeentry.pack(side=TK.LEFT)
        row4=TK.Frame(row_main, pady=5)               #选项确定和取消  
        row4.pack(side=TK.TOP, fill=TK.X)
        TK.Button(row4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
        row3=TK.Frame(self, relief=TK.GROOVE, borderwidth=2, pady=5)                
        row3.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(row3, text='Stock code such as 600292, Date format is yyyy-mm-dd')
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
    def Confirm(self):       
        self.code2=self.stockcode2.get()
        self.stdate2=self.starttime2.get()
        detail=tickData(self.code2, self.stdate2)
        detail.plotTickLine()
        self.plotinfo2=self.code2+'_'+self.stdate2+'.png'
        detgraph=figureplot(self.plotinfo2, self.code2)
    def Cancel(self):
        self.destroy()      

class seclayersim(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Stock Price Simulator")
        self.resizable(width=False, height=False)
        simfont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        TK.Label(self, text='Please Enter the following information', font=simfont).pack(side=TK.TOP)
        row_mainbal=TK.Frame(self,relief=TK.GROOVE, borderwidth=2 )
        row_mainbal.pack(side=TK.TOP, fill=TK.X)
        row_bal3=TK.Frame(row_mainbal, pady=5)
        row_bal3.pack(side=TK.TOP, fill=TK.X)
        stock_code3=TK.Label(row_bal3, text='Balance',width=15)
        stock_code3.pack(side=TK.LEFT)
        self.balance=TK.DoubleVar()
        balance_entry=TK.Entry(row_bal3, textvariable=self.balance,width=10)
        balance_entry.pack(side=TK.LEFT)
        startdate=TK.Label(row_bal3, text='Start Date',width=15)
        startdate.pack(side=TK.LEFT)
        self.sdate=TK.StringVar()
        Date_entry=TK.Entry(row_bal3, textvariable=self.sdate,width=10)
        Date_entry.pack(side=TK.LEFT)
        simtime=TK.Label(row_bal3, text='Start Time (Optional)',width=20)
        simtime.pack(side=TK.LEFT)
        self.stime=TK.StringVar()
        self.stime.set('00:00:00')
        time_entry=TK.Entry(row_bal3, textvariable=self.stime,width=10)
        time_entry.pack(side=TK.LEFT)
        row_bal4=TK.Frame(row_mainbal)
        row_bal4.pack(side=TK.TOP, fill=TK.X)
        TK.Label(row_bal4, text='Fee (Optional)',width=15).pack(side=TK.LEFT)
        self.fee=TK.IntVar()
        self.fee.set(0.0005)
        TK.Entry(row_bal4,textvariable=self.fee, width=10).pack(side=TK.LEFT)
        TK.Label(row_bal4, text='Tax (Optional)',width=15).pack(side=TK.LEFT)
        self.tax=TK.IntVar()
        self.tax.set(0.001)
        TK.Entry(row_bal4,textvariable=self.tax, width=10).pack(side=TK.LEFT)
        TK.Button(row_bal4, text='Cancel', width=12, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row_bal4, text='Confirm', width=12, command=self.Confirm, padx=4).pack(side=TK.RIGHT) #self.drawfigure())
        notification=TK.Frame(self, relief=TK.GROOVE,borderwidth=2, pady=10)
        notification.pack(side=TK.TOP, fill=TK.X)
        note1=TK.Frame(notification)
        note1.pack(side=TK.TOP, fill=TK.X)
        note2=TK.Frame(notification)
        note2.pack(side=TK.TOP, fill=TK.X)
        note3=TK.Frame(notification)
        note3.pack(side=TK.TOP, fill=TK.X)
        note4=TK.Frame(notification)
        note4.pack(side=TK.TOP, fill=TK.X)
        note5=TK.Frame(notification)
        note5.pack(side=TK.TOP, fill=TK.X)
        TK.Label(note1, text='(1) Balance is the initial money for your simulation').pack(side=TK.LEFT)
        TK.Label(note2, text='(2) Start date is the starting date for simulation (format yyyy-mm-dd)').pack(side=TK.LEFT)
        TK.Label(note3, text='(3) Start time for simulation is optional. (foramt hh:mm:ss, 00:00:00 if not indicated)').pack(side=TK.LEFT)
        TK.Label(note4, text='(4) Fee is optional. (0.0005 if not indicated)').pack(side=TK.LEFT)
        TK.Label(note5, text='(5) Tax is optional. (0.001 if not indicated)').pack(side=TK.LEFT)
    def Confirm(self):
        sts=ss.stockSimulate(self.balance.get(), self.sdate.get(), self.stime.get(), self.fee.get(), self.tax.get())
        thirdsim=thilayersimulate(sts)
        self.destroy()
    def Cancel(self):
        self.destroy()

class thilayersimulate(TK.Toplevel):
    def __init__(self, sts):
        super().__init__()
        self.sts=sts
        self.title("Stock Price Simulator")
        self.resizable(width=False, height=False)
        expfont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        row_sim3=TK.Frame(self, relief=TK.RIDGE, borderwidth=4)
        row_sim3.pack(side=TK.TOP, fill=TK.X)
        row_explain1=TK.Frame(row_sim3)
        row_explain1.pack(side=TK.TOP, fill=TK.X, pady=5)
        TK.Label(row_explain1, text='Operation Region', font=expfont).pack(side=TK.LEFT)
        row_bal=TK.Frame(row_sim3)
        row_bal.pack(side=TK.TOP, fill=TK.X)
        stock_code2=TK.Label(row_bal, text='Stock Code',width=15)
        stock_code2.pack(side=TK.LEFT)
        self.stockcode3=TK.StringVar()
        code_entry=TK.Entry(row_bal, textvariable=self.stockcode3,width=10)
        code_entry.pack(side=TK.LEFT)
        row_sim1=TK.Frame(row_sim3, pady=5)
        row_sim1.pack(side=TK.TOP, fill=TK.X)
        row_sim2=TK.Frame(row_sim3)
        row_sim2.pack(side=TK.TOP, fill=TK.X)
        self.optype=TK.IntVar()
        self.optype.set(1)
        TK.Radiobutton(row_sim2, text='Execute Buy', value=1, variable=self.optype).pack(side=TK.LEFT)
        TK.Radiobutton(row_sim2, text='Execute Sell', value=2, variable=self.optype).pack(side=TK.LEFT)
        share=TK.Label(row_bal, text='Share Amount',width=15)
        share.pack(side=TK.LEFT)      
        self.shareamount=TK.IntVar()
        share_entry=TK.Entry(row_bal, textvariable=self.shareamount,width=10)
        share_entry.pack(side=TK.LEFT)
        Dateop=TK.Label(row_sim1, text="Operation Date", width=15)
        Dateop.pack(side=TK.LEFT)
        self.opdate=TK.StringVar()
        Date_entry=TK.Entry(row_sim1, textvariable=self.opdate,width=10)
        Date_entry.pack(side=TK.LEFT)
        Timeop=TK.Label(row_sim1, text="Operation Time", width=15)
        Timeop.pack(side=TK.LEFT)
        self.optime=TK.StringVar()
        Time_entry=TK.Entry(row_sim1, textvariable=self.optime,width=10)
        Time_entry.pack(side=TK.LEFT)
        TK.Button(row_sim2, text='Cancel', width=8, command=self.Cancel).pack(side=TK.RIGHT, padx=12) #self.quit())
        TK.Button(row_sim2, text='Execute', width=8, command=self.Execute).pack(side=TK.RIGHT) #self.drawfigure())
        row_sim4=TK.Frame(self, relief=TK.RIDGE, borderwidth=4)
        row_sim4.pack(side=TK.TOP, fill=TK.X)
        row_explain3=TK.Frame(row_sim4)
        row_explain3.pack(side=TK.TOP, fill=TK.X, pady=5)
        TK.Label(row_explain3, text='Consult History', font=expfont).pack(side=TK.LEFT)
        row_sim5=TK.Frame(row_sim4)
        row_sim5.pack(side=TK.TOP, fill=TK.X)
        TK.Label(row_sim5, text='Stock code', width=15).pack(side=TK.LEFT)
        self.code4=TK.StringVar()
        TK.Entry(row_sim5, textvariable=self.code4, width=10).pack(side=TK.LEFT)
        TK.Label(row_sim5, text='Start Date', width=15).pack(side=TK.LEFT)
        self.simsdate=TK.StringVar()
        TK.Entry(row_sim5, textvariable=self.simsdate, width=10).pack(side=TK.LEFT)
        row_sim6=TK.Frame(row_sim4)
        row_sim6.pack(side=TK.TOP, fill=TK.X)
        TK.Label(row_sim6, text='End Date', width=15).pack(side=TK.LEFT)
        self.simedate=TK.StringVar()
        TK.Entry(row_sim6, textvariable=self.simedate, width=10).pack(side=TK.LEFT)
        TK.Button(row_sim6, text='Confirm', width=8, command=self.Confirm).pack(side=TK.RIGHT,padx=12) #self.quit())
        ophis=TK.Frame(self, relief=TK.RIDGE, borderwidth=4)
        ophis.pack(side=TK.TOP)
        labelframe=TK.Frame(ophis)
        labelframe.pack(side=TK.TOP, fill=TK.X, pady=5)
        TK.Label(labelframe,  text='Operation History', font=expfont).pack(side=TK.LEFT)
        hisframe=TK.Frame(ophis)
        hisframe.pack(side=TK.TOP, fill=TK.X)
        self.yscroll=TK.Scrollbar(hisframe, orient=TK.VERTICAL)
        self.yscroll.grid(row=0, column=1, sticky=TK.N+TK.S)
        self.xscroll=TK.Scrollbar(hisframe, orient=TK.HORIZONTAL)
        self.xscroll.grid(row=1, column=0, sticky=TK.E+TK.W)
        self.ophistory=TK.Listbox(hisframe, width=52,  height=6, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.ophistory.grid(row=0, column=0, sticky=TK.N+TK.S+TK.E+TK.W)
        self.xscroll['command']=self.ophistory.xview
        self.yscroll['command']=self.ophistory.yview
        Accountinfo=TK.Frame(self, relief=TK.RIDGE, borderwidth=4)
        Accountinfo.pack(side=TK.TOP)
        accountframe=TK.Frame(Accountinfo)
        accountframe.pack(side=TK.TOP, fill=TK.X, pady=5)
        TK.Label(accountframe,  text='Account Information', font=expfont).pack(side=TK.LEFT)
        balanceframe=TK.Frame(Accountinfo)
        balanceframe.pack(side=TK.TOP, fill=TK.X)
        self.smybalance=TK.IntVar()
        self.smybalance.set(sts.showbalance)
        TK.Label(balanceframe, text='Balance').pack(side=TK.LEFT)
        self.balentry=TK.Entry(balanceframe, textvariable=self.smybalance)
        self.balentry.pack(side=TK.LEFT)
        accframe=TK.Frame(Accountinfo)
        accframe.pack(side=TK.TOP, fill=TK.X)
        self.ayscroll=TK.Scrollbar(accframe, orient=TK.VERTICAL)
        self.ayscroll.grid(row=0, column=1, sticky=TK.N+TK.S)
        self.axscroll=TK.Scrollbar(accframe, orient=TK.HORIZONTAL)
        self.axscroll.grid(row=1, column=0, sticky=TK.E+TK.W)
        self.aop=TK.Listbox(accframe, width=52, height=6, xscrollcommand=self.axscroll.set, yscrollcommand=self.ayscroll.set)
        self.aop.grid(row=0, column=0, sticky=TK.N+TK.S+TK.E+TK.W)
        self.axscroll['command']=self.aop.xview
        self.ayscroll['command']=self.aop.yview
        #self.aop.insert(TK.END, "this is a test")
        #ophistory.pack(side=TK.TOP, fill=TK.X)
    def Confirm(self):
        self.newcode=self.code4.get()
        self.newst=self.simsdate.get()
        self.newen=self.simedate.get()
        conhistory=historyData(self.newcode,self.newst,self.newen)
        conhistory.plotCandleStick(ma5=True,ma10=True,ma20=True,volume=True)
        self.plotinfocon=self.newcode+'_'+self.newst+'_'+self.newen+'.png'
        hisgraph=figureplot(self.plotinfocon, self.newcode)
    def Cancel(self):
        self.destroy()
    def Execute(self):
        self.opcode=self.stockcode3.get()
        self.opshare=self.shareamount.get()
        self.operationdate=self.opdate.get()
        self.operationtime=self.optime.get()
        if((self.optype.get())==1):
            self.sts.buy(self.opcode, self.opshare,self.operationdate, self.operationtime)
            if(self.sts.oplog==0):
                a=self.operationdate+'  '+self.operationtime+'  buy  '+self.opcode+'  '+str(self.opshare)+' share  Success'
            else:
                a=self.operationdate+'  '+self.operationtime+'  buy  '+self.opcode+'  '+str(self.opshare)+' share  Fail('+self.sts.buystring+')'
                buyerrormsg=simmsg(self.sts.buystring)
            self.ophistory.insert(TK.END, a)
            
        if((self.optype.get())==2):
            self.sts.sell(self.opcode, self.opshare, self.operationdate, self.operationtime)
            
            if(self.sts.opselllog==0):
                b=self.operationdate+'  '+self.operationtime+'  sell  '+self.opcode+'  '+str(self.opshare)+' share  Success'
            else:
                b=self.operationdate+'  '+self.operationtime+'  sell  '+self.opcode+'  '+str(self.opshare)+' share  Fail('+self.sts.sellstring+')'
                sellerrormsg=simmsg(self.sts.sellstring)
            self.ophistory.insert(TK.END, b)
        self.showaccount() 
        
    def showaccount(self):
        self.sts.showAccount()
        self.smybalance.set(self.sts.showbalance)
        self.aop.delete(0, TK.END)
        #self.aop.insert(TK.END, self.sts.showbalance)
        for code in self.sts.showstocklist.keys():
            l=code+':     '+str(self.sts.showstocklist[code])+' share'
            self.aop.insert(TK.END, l)
        
class simmsg(TK.Toplevel):
    def __init__(self, msg):
        super().__init__()
        self.title('Error')
        self.resizable(width=False, height=False)
        TK.Label(self, text=msg, bg='white', pady=5).pack(side=TK.TOP)
        buttonframe=TK.Frame(self, pady=5)
        buttonframe.pack(side=TK.TOP, fill=TK.X)
        TK.Button(buttonframe, text='Confirm', width=12, command=self.opConfirm).pack(side=TK.TOP) #self.quit())
    def opConfirm(self):
        self.destroy()
        
if __name__=='__main__':
    haha=mainGUI()
    haha.mainloop()
        