#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 1 : Installing necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
get_ipython().system('pip install yfinance matplotlib pandas seaborn')


# In[2]:


# 2 : Importing necessary modules
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import yfinance as yf
import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np


# In[3]:


# 3 : Data getting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# we will take the values of Gold, Silver, the US dollar index, and the S&P 500 as tickers.
tickers = ['GC=F', 'SI=F','DX-Y.NYB','^GSPC']

# and we can then  find the closing prices of the four indexes every week for a range of time, here i used period_ so i can change if needed
period_ = ('5y')

#then we can find the daily values of each over the period 'period_'
gold = yf.Ticker(tickers[0]).history(period = period_, interval = '1d')['Close']
silver = yf.Ticker(tickers[1]).history(period = period_, interval = '1d')['Close']
dollar = yf.Ticker(tickers[2]).history(period =period_, interval = '1d')['Close']
sp = yf.Ticker(tickers[3]).history(period = period_, interval = '1d')['Close']

# now,  we need a way to group all data in one table and rename the columns: 
data_raw = pd.concat([gold, silver, dollar, sp], axis=1)
data_raw.columns = ['Gold', 'Silver', 'US Dollar', 'S&P 500']

# then i found one problem being that many data were missing so i used the .dropna function to erase those missing data
clean_data = data_raw.dropna()

#and we can check to see if any data is missing a second time using :
print(clean_data.isnull().isnull().sum())


# In[4]:


# 4 now to see if the dataframe is updated correctly : 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean_data.head()


# In[5]:


# and we can get a lot of information using describe : 
clean_data.describe()


# In[6]:


# 5 : we now want to create a correlation heatmap, in order to know how relevant other assets are to the main investing asset (Gold)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


corr = clean_data.corr()
plt.figure(figsize=(10, 5))
sns.heatmap(corr, annot=True)
corr.style.background_gradient(cmap = "bwr")


# as we can see gold is very correlated to silver and the sp 500. on the other hand, the dollar and gold are rarely moving in relationship. 

# In[7]:


# 6 : Another good measure of the link between gold prices, silver prices, the US dollar index and the S&P 500 is the regression analysis. 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fig, axes = plt.subplots(1, 3, figsize=(18, 6))


sns.regplot(x="S&P 500", y="Gold", data=clean_data, ax=axes[0])
axes[0].set_title('S&P 500 vs Gold')

sns.regplot(x="Silver", y="Gold", data=clean_data, ax=axes[1])
axes[1].set_title('Silver vs Gold')

sns.regplot(x="US Dollar", y="Gold", data=clean_data, ax=axes[2])
axes[2].set_title('US Dollar vs Gold')

plt.show()


# once again, it is clear that gold and S&P are most relatedwhen the dollar depends on many other elements. we can't upload the project and ask you to install a webdriver, but when i did i could connect to tradingviews and obtain the gold prices every five seconds. using the regression coefficients above could have allowed us to create accurate ratios 

# In[8]:


clean_data['Gold_MA_3'] = clean_data['Gold'].rolling(window=3).mean()
clean_data['Gold_MA_6'] = clean_data['Gold'].rolling(window=6).mean()

#using the entire data, the moving average was useless. we therefore tried to isolate a part of the data, 60 days to be precise.

last_2M_data = clean_data.loc[clean_data.index >= clean_data.index[-1] - timedelta(days=60)]
last_2M_data = last_2M_data.copy()

# to highlight the most obvious support lines using the moving averages, we need to create the signals used in the graph (we used those in class)

last_2M_data['signal'] = np.where(last_2M_data['Gold_MA_3'] > last_2M_data['Gold_MA_6'], 1.0, 0.0)
last_2M_data['signal'] = last_2M_data['signal'].shift()
last_2M_data['positions'] = last_2M_data['signal'].diff()

plt.figure(figsize=(12, 6))
plt.plot(last_2M_data.index, last_2M_data['Gold'], label='Gold Price')
plt.plot(last_2M_data.index, last_2M_data['Gold_MA_3'], label='Short MA (3 days)')
plt.plot(last_2M_data.index, last_2M_data['Gold_MA_6'], label='Long MA (6 days)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)

plt.plot(last_2M_data.loc[last_2M_data.positions == 1.0].index, last_2M_data.Gold_MA_3[last_2M_data.positions == 1.0],
         '^', markersize=10, color='g', label='Buy')
plt.plot(last_2M_data.loc[last_2M_data.positions == -1.0].index, last_2M_data.Gold_MA_3[last_2M_data.positions == -1.0],
         'v', markersize=10, color='r', label='Sell')

plt.legend(['Gold', 'MA (3 days)', 'MA (6 days)', 'Buy', 'Sell'])
plt.title('Gold prices evolution and moving averages with buy/sell signals')
plt.show()


# In[9]:


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
last_week_data = yf.Ticker("GC=F").history(period = "1wk", interval = "1h")['Close']

high = last_week_data.max()
low = last_week_data.min()


retracements = [0, 23.6, 38.2, 50, 61.8, 100]
fib_levels = [(high - low) * level / 100 + low for level in retracements]

colors = ['red', 'orange', 'yellow', 'blue', 'green', 'lightgreen']

for level, color in zip(fib_levels, colors):
    plt.axhline(y=level, color=color, linestyle='--', label=f'Retracement ({retracements[fib_levels.index(level)]:.1f}%)')


plt.plot(last_week_data.index, last_week_data, label='Gold Price')
plt.gcf().autofmt_xdate()
plt.gca().xaxis_date()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.legend()
plt.title('Fibonacci retracement levels over the past week on gold prices')
plt.xlabel('Date')
plt.ylabel('Gold Price')
plt.show()


# 
# this graph is used by traders to assess the level of risk on investments of shorter term. the numbers are derived from fibonnaci sequence, when dividing n by n+1, or n by n+2. combined with the moving average, the data gives a relevant insight on the future price direction. they are reference support lines : when the price hits a low, it is interesting to put a stop-loss at one of the percentages in the legend. the golden ratios are generally considered to be 23.6 and 38.2 % of retracement to reenter the market.

# In[ ]:





# In[ ]:




