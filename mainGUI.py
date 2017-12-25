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
from arimaPredict import *
from historyData import *
from tickData import *
import tkinter.font as tkfont

class figureplot(TK.Toplevel):  #单独构造画图类
    def __init__(self, plotinfo, stockcode):
        super().__init__()
        self.title("Stock Price Viewer")
        tfont=tkfont.Font(family='Helvetica', size=10, weight=tkfont.BOLD)
        plottitle=TK.Frame(self, bg='white')
        plottitle.pack()
        plotlabel=TK.Label(plottitle,text='Stock'+'  '+stockcode,font=tfont, bg='white')
        plotlabel.pack(pady=5)
        #figplot=TK.Frame(self)
        #figplot.pack(side=TK.TOP, fill=TK.X)
        self.img = ImageTk.PhotoImage(file=plotinfo)
        TK.Label(self, image=self.img).pack(side=TK.TOP) 
'''        
class modifiedap(arimaPredict):
    def __init__(self,code,date):
        self.code=code;
        self.date=date;
        self.data=ts.get_hist_data(code,"2015-01-01",date);
    def predictor(self,days,ifCompare=False):
        fit=auto_arima(list(reversed(self.data.close.tolist())),start_p=1,max_p=9,start_q=1,max_q=6,d=1,max_d=5,seasonal=False)
        onePredict=fit.predict(n_periods=days)
        x=range(0,days)
        y=ts.get_hist_data(self.code,start=self.date,end=str(date.today()))
        if(ifCompare):
            if(pd.nrow(y)>days):
                plt.plot(x,list(reversed(y.close.tolist()))[1:(days+1)],'g')
            else:
                plt.plot(x[0:(pd.nrow(y)-1)],list(reversed(y.close.tolist())),'g')
        fig=plt.plot(x,onePredict,'r')
        fig.savefig(self.code+'_'+self.date+'_'+str(days)+'.png')
'''     
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
        premenu.add_command(label='Arima Self-correlation', accelerator='Ctrl+A', compound='left', underline=0, command=self.callarima)
        premenu.add_separator()
        premenu.add_command(label='Lagrange Interpolation', accelerator='Ctrl+L', compound='left', underline=0)
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
    def secopyright(self):
        thirdcopy=showcopyright()
    def trysimulation(self):
        thirdsim=seclayersim()
        
class seclayerarima(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('ARIMA Prediction')
        arima1=TK.Frame(self)                
        arima1.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(arima1, text='股票代码如600292，日期格式为yyyy-mm-dd，如2017-01-01',pady=20)
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
        arima2=TK.Frame(self)               #股票代码
        arima2.pack(side=TK.TOP, fill=TK.X)    
        arima_code=TK.Label(arima2, text='Stock Code',width=10)
        arima_code.pack(side=TK.LEFT)
        self.arimacode=TK.StringVar()
        arimaentry1=TK.Entry(arima2, textvariable=self.arimacode,width=38)
        arimaentry1.pack(side=TK.LEFT)
        arima3=TK.Frame(self)             #查询时间
        arima3.pack(side=TK.TOP, fill=TK.X)   
        arimastart=TK.Label(arima3, text='Start Date', width=10)
        arimastart.pack(side=TK.LEFT)
        self.arimatime=TK.StringVar()
        arimatimeentry=TK.Entry(arima3,textvariable=self.arimatime, width=13)
        arimatimeentry.pack(side=TK.LEFT)
        arimaend=TK.Label(arima3, text='Days', width=10)
        arimaend.pack(side=TK.LEFT)
        self.arima_days=TK.IntVar()
        dayentry=TK.Entry(arima3,textvariable=self.arima_days, width=13)
        dayentry.pack(side=TK.LEFT)        
        arima4=TK.Frame(self)               #选项确定和取消  
        arima4.pack(side=TK.TOP, fill=TK.X, pady=15)
        TK.Button(arima4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(arima4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
    def Confirm(self):
        print('Not finished')
        '''
        ap=modifiedap(self.arimacode.get(), self.arimatime.get())
        ap.predictor(self.arima_days.get())
        self.plotinfoap=self.arimacode.get()+'_'+self.arimatime.get()+'_'+str(self.arima_days.get())+'.png'
        arimagraph=figureplot(self.plotinfoap, self.arimacode.get())
        '''
    def Cancel(self):
        self.destroy()
        
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
        self.geometry('350x180')         #history data窗口大小
        self.resizable(width=False, height=False)
        row3=TK.Frame(self)                
        row3.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(row3, text='股票代码如600292，日期格式为yyyy-mm-dd，如2017-01-01',pady=20)
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
        row1=TK.Frame(self)               #股票代码
        row1.pack(side=TK.TOP, fill=TK.X)    
        stock_code=TK.Label(row1, text='Stock Code',width=10)
        stock_code.pack(side=TK.LEFT)
        self.stockcode=TK.StringVar()
        codeentry=TK.Entry(row1, textvariable=self.stockcode,width=38)
        codeentry.pack(side=TK.LEFT)
        row2=TK.Frame(self)             #查询时间
        row2.pack(side=TK.TOP, fill=TK.X)   
        start_time=TK.Label(row2, text='Start Date', width=10)
        start_time.pack(side=TK.LEFT)
        self.starttime=TK.StringVar()
        starttimeentry=TK.Entry(row2,textvariable=self.starttime, width=13)
        starttimeentry.pack(side=TK.LEFT)
        end_time=TK.Label(row2, text='End Date', width=10)
        end_time.pack(side=TK.LEFT)
        self.endtime=TK.StringVar()
        endtimeentry=TK.Entry(row2,textvariable=self.endtime, width=13)
        endtimeentry.pack(side=TK.LEFT)        
        row4=TK.Frame(self)               #选项确定和取消  
        row4.pack(side=TK.TOP, fill=TK.X, pady=15)
        TK.Button(row4, text='Cancel', width=6, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row4, text='Confirm', width=6, command=self.Confirm).pack(side=TK.RIGHT) #self.drawfigure())
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
        self.title("See Day Data")
        rowl=TK.Frame(self)                
        rowl.pack(side=TK.TOP, fill=TK.X)
        inputexplain=TK.Label(rowl, text='股票代码如600292，时间格式为yyyy-mm-dd，如2017-01-01',pady=15)
        inputexplain.pack(side=TK.LEFT, fill=TK.X)
        row1=TK.Frame(self)               #股票代码
        row1.pack(side=TK.TOP, fill=TK.X)    
        stock_code=TK.Label(row1, text='Stock Code',width=10)
        stock_code.pack(side=TK.LEFT)
        self.stockcode2=TK.StringVar()
        codeentry=TK.Entry(row1, textvariable=self.stockcode2,width=35)
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
        detgraph=figureplot(self.plotinfo2, self.code2)
    def Cancel(self):
        self.destroy()      

class seclayersim(TK.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Stock Price Simulator")
        self.resizable(width=False, height=False)
        row_bal3=TK.Frame(self, pady=5)
        row_bal3.pack(side=TK.TOP, fill=TK.X)
        stock_code3=TK.Label(row_bal3, text='Balance',width=15)
        stock_code3.pack(side=TK.LEFT)
        self.balance=TK.IntVar()
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
        row_bal4=TK.Frame(self)
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
        TK.Label(note2, text='(2) Start date is the starting date for simulation').pack(side=TK.LEFT)
        TK.Label(note3, text='(3) Start time for simulation is optional. (00:00:00 if not indicated)').pack(side=TK.LEFT)
        TK.Label(note4, text='(4) Fee is optional. (0.0005 if not indicated)').pack(side=TK.LEFT)
        TK.Label(note5, text='(5) Tax is optional. (0.001 if not indicated)').pack(side=TK.LEFT)
    def Confirm(self):
        sts=ss.stockSimulate(self.balance.get(), self.sdate.get(), self.stime.get(), self.fee.get(), self.tax.get())
        thirdsim=thilayersimulate(sts)
    def Cancel(self):
        self.destroy()

class thilayersimulate(TK.Toplevel):
    def __init__(self, sts):
        super().__init__()
        self.title("Stock Price Simulator")
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
        self.stockcode2=TK.StringVar()
        code_entry=TK.Entry(row_bal, textvariable=self.stockcode2,width=10)
        code_entry.pack(side=TK.LEFT)
        row_sim1=TK.Frame(row_sim3, pady=5)
        row_sim1.pack(side=TK.TOP, fill=TK.X)
        row_sim2=TK.Frame(row_sim3)
        row_sim2.pack(side=TK.TOP, fill=TK.X)
        self.var=TK.IntVar()
        self.var.set(1)
        TK.Radiobutton(row_sim2, text='Execute Buy', value=1, variable=self.var).pack(side=TK.LEFT)
        TK.Radiobutton(row_sim2, text='Execute Sell', value=2, variable=self.var).pack(side=TK.LEFT)
        share=TK.Label(row_bal, text='Share Amount',width=15)
        share.pack(side=TK.LEFT)      
        self.shareamount=TK.IntVar()
        share_entry=TK.Entry(row_bal, textvariable=self.shareamount,width=10)
        share_entry.pack(side=TK.LEFT)
        Dateop=TK.Label(row_sim1, text="Operation Date", width=15)
        Dateop.pack(side=TK.LEFT)
        self.opdate=TK.IntVar()
        Date_entry=TK.Entry(row_sim1, textvariable=self.opdate,width=10)
        Date_entry.pack(side=TK.LEFT)
        Timeop=TK.Label(row_sim1, text="Operation Time", width=15)
        Timeop.pack(side=TK.LEFT)
        self.optime=TK.IntVar()
        Time_entry=TK.Entry(row_sim1, textvariable=self.optime,width=10)
        Time_entry.pack(side=TK.LEFT)
        TK.Button(row_sim2, text='Cancel', width=8, command=self.Cancel).pack(side=TK.RIGHT) #self.quit())
        TK.Button(row_sim2, text='Execute', width=8, command=self.Execute).pack(side=TK.RIGHT) #self.drawfigure())
        
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
        