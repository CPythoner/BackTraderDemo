import backtrader as bt
from backtrader import *
from datetime import datetime

# Create a subclass of Strategy to define the indicators and logic

class Strategy001(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

    def log(self,txt,dt=None):
        # log记录函数。
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(),txt))

    def next(self):
        self.log('Close 收盘价，%.2f' % self.dataclose[0])

print('\n#1，设置 BT 量化回测程序入口')
cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

print('\n#2，设置BT回测初始参数及策略')
print('\n\t#2-1，设置BT回测初始参数：起始资金等')
dmoney0 = 100000.0
cerebro.broker.setcash(dmoney0)
dcash0 = cerebro.broker.startingcash

print('\n\t#2-2，设置数据文件，需要按时间字段正序排序')
rs0 = os.path.abspath(os.path.dirname(__file__)) + '/../data/'
filename = '002046.SZ.csv'
fdat = rs0 + filename
print('\t@数据文件名：', fdat)

print('\t 设置数据BT回测运算：起始时间、结束时间')
print('\t 数据文件，可以是股票期货、外汇黄金、数字货币等交易数据')
print('\t 格式为：标准OHLC格式，可以是日线、分时数据')

t0stx,t9stx = datetime(2018, 1, 1),datetime(2018, 12, 31)
data = bt.feeds.YahooFinanceCSVData(dataname=fdat,
                                 fromdate=t0stx,
                                 todate=t9stx)
cerebro.adddata(data)  # Add the data feed


print('\n\t#2-3，添加BT量化回测程序，对应的策略参数')
cerebro.addstrategy(Strategy001)

print('\n#3，调用BT回测入口程序，开始执行run量化回测运算')
cerebro.run()

print('\n#4，完成BT量化回测运算')
dval9 = cerebro.broker.getvalue()
print('\t 起始资金Starting Portfolio Value:%.2f' % dcash0)
print('\t 资产总值Final Portfolio Value:%.2f' % dval9)

print('\n#5，绘制BT量化分析图形')
cerebro.plot()  # and plot it with a single command
