import pandas as pd
import numpy as np
from pandas_datareader import data
# import matplotlib.pyplot as plt


start_date='2001-01-01'
end_date='2019-12-31'


def load_financial_data(token, start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print('File data found...reading the data')
    except FileNotFoundError:
        print('File not found...downloading the data')
        df = data.DataReader(token, 'yahoo', start_date, end_date)
        df.to_pickle(output_file)
    return df

goog_token = 'GOOG'
goog_data = load_financial_data(goog_token, start_date=start_date, end_date=end_date, output_file='goog_data_large.pkl')

spy_token = 'SPY'
spy_data = load_financial_data(spy_token, start_date=start_date, end_date=end_date, output_file='spy_data_large.pkl')


totaldata = pd.DataFrame(index=goog_data.index)
totaldata['spy'] = spy_data['Adj Close']
totaldata['change'] = goog_data['Adj Close'] - goog_data['Adj Close'].shift(1)

sig_data = pd.DataFrame(index=goog_data.index)
sig_data['Close'] = goog_data['Adj Close']
sig_data['Change'] = sig_data['Close'].diff()
sig_data['signal'] = np.where(sig_data['Change']>0, 1, 0)
sig_data['order'] = 0
sig_data['order'] = sig_data['signal'].diff()

position = 0
positions = []

profit = 0
profits = []
last_buy = 0
buy_price = 0
buy_price_list = []
openpnl = 0
openpnls = []
closepnl = 0
closepnls = []
close = sig_data['Close']
for i, close_price in enumerate(close):
  
  if sig_data['order'].iloc[i] > 0:
    position += 1
    positions.append(position)
    last_buy = sig_data['Close'].iloc[i]
    buy_price = last_buy
    buy_price_list.append(buy_price)

    profit = 0
    profits.append(profit)            
    closepnls.append(closepnl)
  elif sig_data['order'].iloc[i] < 0:
    position -= 1
    positions.append(position)
    last_sell = sig_data['Close'].iloc[i]
    buy_price = 0
    buy_price_list.append(buy_price)
    
    profit = last_sell - last_buy
    profits.append(profit)
    
    closepnl += profit
    closepnls.append(closepnl)
  else:
    positions.append(position)
    if position > 0:
      buy_price = last_buy
    else:
      buy_price = 0
    buy_price_list.append(buy_price)

    profit = 0
    profits.append(profit)
    
    closepnls.append(closepnl)


sig_data['position'] = positions
sig_data['profit'] = profits
sig_data['buy_price'] = buy_price_list
sig_data['openpnl'] = (sig_data['Close'] - sig_data['buy_price']) * sig_data['position']
sig_data['closepnl'] = closepnls

sig_data.to_csv('test.csv')
print(sig_data[['Close', 'position','buy_price', 'openpnl', 'closepnl']])
# print(sig_data[['Close','Change', 'position','buy_price', 'openpnl', 'closepnl']])
# print(sig_data[['Change', 'position','buy_price', 'closepnl']])