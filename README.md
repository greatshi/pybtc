# PyBTC: 一个加密货币的自动交易程序


架构
=======
计划在原有基础上更新版本
[Architecture](fig/architecture.png)
做成事件驱动版本
使用RabbitMQ传送事件
SQLite存储行情信息
MongoDB存储交易相关信息

功能
=======
可以实现自定义币种、价格、数量的左侧交易或右侧交易<br />
设定买入、卖出价格，自动循环交易<br />
实现了网站 Python 版的 API, 可以自己开发交易策略<br />
exe暂不支持 coinut<br />
目前只能在 coinut 进行交易(strategy_ut.py)<br />
在dist文件夹中双击 strategy.exe 即可运行，支持 Win7-Win10 32bit & 64bit<br />
strategy.exe SHA256: `bd954b185be34a2aca3c31aa988ae3e8100403f072eacfd817a55dca21d91f02`<br />
w9xpopen.exe SHA256: `243c34e56805f87f0254d59826fbab1d062da19308644046a3a92997d86d0bdb`<br />
使用 py2exe 打包程序

系统需求
=======
Mac、Linux、Win 都可运行<br />
Win需要安装: Python 2.7<br />

运行
=======
在[btctrade.com](https://www.btctrade.com)申请“获取API认证的公钥和私钥”<br />
在[coinut.com](https://coinut.com)申请“REST API Key”<br />
在命令行中运行<br />
$python strategy.py<br />
首次运行需要输入申请的公钥和私钥，所有的输入使用空格分隔<br />

交易参数
=======
[btctrade](https://www.btctrade.com)<br />
{left, right} {btc, eth, ltc, doge, ybc} {amount} {price} {price}<br />

[coinut](https://coinut.com)<br />
{left, right} {BTCUSDT, ETHUSDT, LTCUSDT} {amount_ratio} {price} {price}<br />

例如
=======
1. 采用左侧交易（left），购买比特币（btc），数量比例(0.7)，买入价（19500），卖出价（21000）<br />
$ python strategy.py<br />Ctrl+C to quit!<br />side coin amount_ratio buy_price sell_price: `left btc 0.7 19500 21000`<br />
$ python strategy.py `left btc 0.7 19500 21000`<br /><br />

2. 采用左侧交易（left），购买比特币（btc），数量比例(0.7)，浮动比例（0.01），止损比例（0.1）<br />
$ python 02_strategy.py `left btc 0.7 0.01 0.1`<br />

3. 自己调用交易函数如下：<br />
```Python
import trade

print trade.get_last_price('btc')
#打印当前比特币的价格

buy_id = trade.trusted_buy('btc', '1', '19500')
#以19500的价格购买一个比特币，buy_id 为单号

sell_id = trade.trusted_sell('btc', '1', '37500')
#以37500的价格出售一个比特币，sell_id 为单号
```

演进计划
=======
使用神经网络预测价格走势，目前在测试 RNN 代码<br />
使用 Django 做一个简单的 Web 应用<br />
