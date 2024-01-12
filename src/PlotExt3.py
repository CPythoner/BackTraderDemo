import backtrader as bt
from backtrader import *
from datetime import datetime


# Create a subclass of Strategy to define the indicators and logic
class MyStrategy(bt.Strategy):
    # 定义MA均线策略的周期参数变量，默认值是15
    params = (("maperiod", 15),)

    def log(self, txt, dt=None):
        # log记录函数
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        # 默认数据，一般使用股票池当中，下标为0的股票，
        # 通常使用close收盘价，作为主要分析数据字段
        self.dataclose = self.datas[0].close

        # 跟踪track交易中的订单（pending orders），成交价格，佣金费用
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 增加一个均线指标：indicator
        # 注意，参数变量maperiod，主要在这里使用
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 检查订单执行状态order.status：
            # Buy/Sell order submitted/accepted to/by broker
            # broker经纪人：submitted提交/accepted接受,Buy买单/Sell卖单
            # 正常流程，无需额外操作
            return

        # 检查订单order是否完成
        # 注意: 如果现金不足，经纪人broker会拒绝订单reject order
        # 可以修改相关参数，调整进行空头交易
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "买单执行BUY EXECUTED,成交价： %.2f,小计 Cost: %.2f,佣金 Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    "卖单执行SELL EXECUTED,成交价： %.2f,小计 Cost: %.2f,佣金 Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("订单Order： 取消Canceled/保证金Margin/拒绝Rejected")

        # 检查完成，没有交易中订单（pending order）
        self.order = None

    def notify_trade(self, trade):
        # 检查交易trade是关闭
        if not trade.isclosed:
            return

        self.log(
            "交易利润OPERATION PROFIT, 毛利GROSS %.2f, 净利NET %.2f"
            % (trade.pnl, trade.pnlcomm)
        )

    def next(self):
        # next函数是最重要的trade交易（运算分析）函数，
        # 调用log函数，输出BT回溯过程当中，工作节点数据包BAR，对应的close收盘价
        self.log("收盘价Close, %.2f" % self.dataclose[0])
        #
        #
        # 检查订单执行情况，默认每次只能执行一张order订单交易，可以修改相关参数，进行调整
        if self.order:
            return
        #
        # 检查当前股票的仓位position
        if not self.position:
            #
            # 如果该股票仓位为0 ，可以进行BUY买入操作，
            # 这个仓位设置模式，也可以修改相关参数，进行调整
            #
            # 使用最简单的MA均线策略
            if self.dataclose[0] < self.sma[0]:
                # 如果当前close收盘价<当前的ma均价
                # ma均线策略，买入信号成立:
                # BUY, BUY, BUY!!!，买！买！买！使用默认参数交易：数量、佣金等
                self.log(
                    "设置买单 BUY CREATE, %.2f, name : %s"
                    % (self.dataclose[0], self.datas[0]._name)
                )

                # 采用track模式，设置order订单，回避第二张订单2nd order，连续交易问题
                self.order = self.buy()

        else:
            # 如果该股票仓位>0 ，可以进行SELL卖出操作，
            # 这个仓位设置模式，也可以修改相关参数，进行调整
            # 使用最简单的MA均线策略
            if self.dataclose[0] > self.sma[0]:
                # 如果当前close收盘价>当前的ma均价
                # ma均线策略，卖出信号成立:
                # 默认卖出该股票全部数额，使用默认参数交易：数量、佣金等
                self.log(
                    "设置卖单SELLE, %.2f, name : %s"
                    % (self.dataclose[0], self.datas[0]._name)
                )

                # 采用track模式，设置order订单，回避第二张订单2nd order，连续交易问题
                self.order = self.sell()


#
# -------------------- kline
tq10_corUp, tq10_corDown = ["#7F7F7F", "#17BECF"]  # plotly
tq09_corUp, tq09_corDown = ["#B61000", "#0061B3"]
tq08_corUp, tq08_corDown = ["#FB3320", "#020AF0"]
tq07_corUp, tq07_corDown = ["#B0F76D", "#E1440F"]
tq06_corUp, tq06_corDown = ["#FF3333", "#47D8D8"]
tq05_corUp, tq05_corDown = ["#FB0200", "#007E00"]
tq04_corUp, tq04_corDown = ["#18DEF5", "#E38323"]
tq03_corUp, tq03_corDown = ["black", "blue"]
tq02_corUp, tq02_corDown = ["red", "blue"]
tq01_corUp, tq01_corDown = ["red", "lime"]
#
tq_ksty01 = dict(
    volup=tq01_corUp, voldown=tq01_corDown, barup=tq01_corUp, bardown=tq01_corDown
)
tq_ksty02 = dict(
    volup=tq02_corUp, voldown=tq02_corDown, barup=tq02_corUp, bardown=tq02_corDown
)
tq_ksty03 = dict(
    volup=tq03_corUp, voldown=tq03_corDown, barup=tq03_corUp, bardown=tq03_corDown
)
tq_ksty04 = dict(
    volup=tq04_corUp, voldown=tq04_corDown, barup=tq04_corUp, bardown=tq04_corDown
)
tq_ksty05 = dict(
    volup=tq05_corUp, voldown=tq05_corDown, barup=tq05_corUp, bardown=tq05_corDown
)
tq_ksty06 = dict(
    volup=tq06_corUp, voldown=tq06_corDown, barup=tq06_corUp, bardown=tq06_corDown
)
tq_ksty07 = dict(
    volup=tq07_corUp, voldown=tq07_corDown, barup=tq07_corUp, bardown=tq07_corDown
)
tq_ksty08 = dict(
    volup=tq08_corUp, voldown=tq08_corDown, barup=tq08_corUp, bardown=tq08_corDown
)
tq_ksty09 = dict(
    volup=tq09_corUp, voldown=tq09_corDown, barup=tq09_corUp, bardown=tq09_corDown
)
tq_ksty10 = dict(
    volup=tq10_corUp, voldown=tq10_corDown, barup=tq10_corUp, bardown=tq10_corDown
)


class MyBuySell(bt.observers.BuySell):
    plotlines = dict(
        # buy=dict(marker='$\u21E7$', markersize=12.0),  #arrow
        # sell=dict(marker='$\u21E9$', markersize=12.0)
        #
        # buy=dict(marker='$++$', markersize=12.0),
        # sell=dict(marker='$--$', markersize=12.0)
        #
        buy=dict(marker="$✔$", markersize=12.0),
        sell=dict(marker="$✘$", markersize=12.0),
    )


# ----------

print("\n#1，设置 BT 量化回测程序入口")
cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

print("\n#2，设置BT回测初始参数及策略")
print("\n\t#2-1，设置BT回测初始参数：起始资金等")
dmoney0 = 100000.0
cerebro.broker.setcash(dmoney0)
dcash0 = cerebro.broker.startingcash

print("\n\t#2-2，设置数据文件，需要按时间字段正序排序")
rs0 = os.path.abspath(os.path.dirname(__file__)) + "/../data/"
filename = "002046.SZ.csv"
fdat = rs0 + filename
print("\t@数据文件名：", fdat)

print("\t 设置数据BT回测运算：起始时间、结束时间")
print("\t 数据文件，可以是股票期货、外汇黄金、数字货币等交易数据")
print("\t 格式为：标准OHLC格式，可以是日线、分时数据")

t0stx, t9stx = datetime(2018, 1, 1), datetime(2018, 12, 31)
data = bt.feeds.YahooFinanceCSVData(dataname=fdat, fromdate=t0stx, todate=t9stx)

cerebro.adddata(data)  # Add the data feed

print("\n\t#2-3，添加BT量化回测程序，对应的策略参数")
print("\n\t# 案例当中，使用的是MA均线策略")
cerebro.addstrategy(MyStrategy)

print("\n\t#2-4，添加broker经纪人佣金，默认为：千一")
cerebro.broker.setcommission(commission=0.001)

print("\n\t#2-5,设置每手交易数目为：10，不再使用默认值：1手")
cerebro.addsizer(bt.sizers.FixedSize, stake=10)

bt.observers.BuySell = MyBuySell

print("\n#3，调用BT回测入口程序，开始执行run量化回测运算")
cerebro.run()

print("\n#4，完成BT量化回测运算")
dval9 = cerebro.broker.getvalue()
kret = (dval9 - dcash0) / dcash0 * 100

print("\t 起始资金Starting Portfolio Value:%.2f" % dcash0)
print("\t 资产总值Final Portfolio Value:%.2f" % dval9)
print("\t ROI投资回报率Return on investment: %.2f %%" % kret)

print("\n#5，绘制BT量化分析图形")
print("\t注意图形当中,最上面的的cash现金，value资产曲线")
print("\n\t分别运行一下各种不同参数的plot绘图命令")
print("\t注意每次运行只运行一条plot，其他的用#注释符号屏蔽")
print("\t部分参数设置后，如果不清除变量，reset运行环境，效果会一直存在")
print("\t注意各种不同参数，引起的图形变化")

# 1 sty-cor+arrow
# cerebro.plot(style='bar',**tq_ksty10)
# cerebro.plot(style="candle", **tq_ksty10)

# 2 volume
# cerebro.plot(style="candle")
# cerebro.plot(style="candle", volume=False)  # 取消volume成交量图形，默认为 True
#cerebro.plot(style="candle", volume=True)
#cerebro.plot(style="candle", volume=True, voloverlay=False)  # volume成交量：采用subplot子图模式，默认为voloverlay=True叠加模式
# cerebro.plot(style="candle", volume=False, voloverlay=False)

# 3
# plot多图拼接，BT版的股市：《清明上河图》
# 注意修改其实日期参数为：空字符串
# numfigs，默认值为：1
cerebro.plot(numfigs=5)
