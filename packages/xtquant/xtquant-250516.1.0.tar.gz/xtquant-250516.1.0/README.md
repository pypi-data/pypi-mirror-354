## 功能
支持python3.13版本

xttrader 支持银证转账
银行信息查询 xttrader.query_bank_info()
银行账户余额查询xttrader.query_bank_amount()
银证转账转入 xttrader.bank_transfer_in()
银证转账转出 xttrader.bank_transfer_out()
银行卡流水记录查询xttrader.query_bank_transfer_stream()

xttrader 支持期货和期权资金划转
权资金转期货 xttrader.ctp_transfer_option_to_future()
期货资金转期权 xttrader.ctp_transfer_future_to_option()

xttrader支持北交所
xtconstant 添加北交所市价报价方式说明

xttrader 交易数据字段调整
委托 XtOrder 新增
股东代码 secu_account
证券名称 instrument_name
成交 XtTrade 新增
股东代码 secu_account
证券名称 instrument_name
持仓 XtPosition 新增
股东代码 secu_account
证券名称 instrument_name
当前价 last_price
盈亏比例 profit_rate
浮动盈亏 float_profit
持仓盈亏 position_profit
开仓日期 open_date（只对期货可用）
账号资金 XtAsset 新增
可取余额 fetch_balance
当前余额 current_balance（当前余额 = 可用资金 + 冻结资金）

xtdata获取数据函数支持以datetime形式传入时间范围

## 数据
合约信息添加交易日字段 TradingDay
xtdata.get_instrument_detail()

支持获取大单统计数据（需要vip权限）
xtdata.get_transactioncount()

支持获取带有分类信息的板块列表（需要投研版本）
xtdata.get_sector_info()

期权合约信息添加期权预估保证金 OptEstimatedMargin（需要投研版本）
xtdata.get_option_detail_data()

郑商所期货、期权品种提供标准化代码的字段（如 MA2504.ZF）（需要投研版本）

xtdata获取数据函数支持ATM市场
xtdata.get_market_data()
xtdata.get_market_data_ex()

BugFix: 订阅数据问题