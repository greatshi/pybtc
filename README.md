<h1>pybtc: 一个自动用于btctrade.com交易的程序</hi>

功能
=======
止损，止盈
可以实现自定义币种、价格、数量的左侧交易或右侧交易
设定买入、卖出价格，自动循环交易
实现了网站Python版的API, 可以自己开发交易策略

更新
=======
在dist文件夹中双击 strategy.exe 即可运行，支持 Win7-Win10 32bit&64bit
<br />使用 py2exe 打包程序

系统需求
=======
Mac、Linux、Win都可运行
Win需要安装: Python 2.7

运行
=======
在btctrade.com申请“获取API认证的公钥和私钥”

在命令行中运行
$python strategy.py

首次运行需要输入申请的公钥和私钥，所有的输入使用空格分隔

交易参数
=======
{left, right} {btc, eth, ltc, doge, ybc} {amount} {price} {price}

例如
=======
采用左侧交易（left），购买比特币（btc），数量（1），买入价（19500），卖出价（21000）

$ python strategy.py<br />Ctrl+C to quit!<br />side coin amount buy_price sell_price: `left btc 1 19500 21000`
<br />

$ python strategy.py `left btc 1 19500 21000`