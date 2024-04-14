#!/usr/bin/env python
# coding: utf-8

# In[177]:


get_ipython().system('pip install yfinance matplotlib pandas')


# In[178]:


import yfinance as yf
import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#we are getting the tickers for gold, the us dollar index, silver, and the SP 500 for comparison
tickers = ['GC=F', 'SI=F','DX-Y.NYB','^GSPC']

# and we can then  find the closing prices of the four indexes every week for a range of time, here i used period_ so i can change if needed
period_ = ('5y')

gold = yf.Ticker(tickers[0]).history(period = period_, interval = '1d')['Close']
silver = yf.Ticker(tickers[1]).history(period = period_, interval = '1d')['Close']
dollar = yf.Ticker(tickers[2]).history(period =period_, interval = '1d')['Close']
sp = yf.Ticker(tickers[3]).history(period = period_, interval = '1d')['Close']

# now,  we need a way to group all data in one table and rename the columns: 
data_raw = pd.concat([gold, silver, dollar, sp], axis=1)
data_raw.columns = ['Gold', 'Silver', 'US Dollar', 'S&P 500']

# then i found one problem being that many data were missing so i used the .dropna function to erase those missing data
clean_data = data_raw.dropna()

#and we can check to see if any data is missing a second time :
print(clean_data.isnull().isnull().sum())


# In[179]:


clean_data.head()


# In[180]:


clean_data.describe()


# In[181]:


corr = clean_data.corr()
plt.figure(figsize=(10, 5))
sns.heatmap(corr, annot=True)
corr.style.background_gradient(cmap = "bwr")

#as we can see gold is very correlated to silver and the sp 500, 


# In[182]:


sns.regplot(x="S&P 500", y="Gold", data=clean_data )


# In[183]:


sns.regplot(x="Silver", y="Gold", data=clean_data )


# In[184]:


sns.regplot(x="US Dollar", y="Gold", data=clean_data )

# this last regression analysis proves again that the relationship between the dollar and the gold price are more complex than between gold, silver and the sp 500.


# In[185]:


plt.figure(figsize=(12,5))
plt.plot(clean_data.index, clean_data['Gold'], label='Gold')
plt.plot(clean_data.index, clean_data['S&P 500'], label='S&P 500')
plt.xlabel('Year')
plt.ylabel('Price')
plt.title('Evolution of Gold and S&P 500 Prices Over the Years')
plt.legend()
plt.show()


# In[188]:


plt.figure(figsize=(12,5))
plt.plot(clean_data.index, clean_data['Silver'], label='Silver')
plt.plot(clean_data.index, clean_data['US Dollar'], label='US Dollar')
plt.xlabel('Year')
plt.ylabel('Price')
plt.title('Evolution of  US Dollar and Silver Prices Over the Years')
plt.legend()
plt.show()


# In[203]:


import matplotlib.pyplot as plt

# Calculate moving averages for gold
clean_data['Gold_MA_3'] = clean_data['Gold'].rolling(window=3).mean()
clean_data['Gold_MA_6'] = clean_data['Gold'].rolling(window=6).mean()

last_2M_data = clean_data.loc[clean_data.index >= clean_data.index[-1] - timedelta(days=60)]

# Plot gold data with moving averages for the last year
plt.figure(figsize=(12, 6))
plt.plot(last_year_data.index, last_2M_data['Gold'], label='Gold Price')
plt.plot(last_year_data.index, last_2M_data['Gold_MA_3'], label='Gold MA (3 days)')
plt.plot(last_year_data.index, last_2M_data['Gold_MA_6'], label='Gold MA (6 days)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.legend(['Gold', 'MA (3 days)', 'MA (6 days)'])
plt.title('Gold prices evolution and moving averages over the past two months')
plt.plot


# In[207]:


import matplotlib.pyplot as plt

clean_data['Gold_MA_3'] = clean_data['Gold'].rolling(window=3).mean()
clean_data['Gold_MA_6'] = clean_data['Gold'].rolling(window=6).mean()

last_year_data = clean_data.loc[clean_data.index >= clean_data.index[-1] - timedelta(days=60)]

last_2M_data = last_year_data.copy()
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

plt.plot(last_2M_data.loc[last_2M_data.positions == 1.0].index, 
         last_2M_data.Gold_MA_3[last_2M_data.positions == 1.0],
         '^', markersize=10, color='g', label='Buy')
plt.plot(last_2M_data.loc[last_2M_data.positions == -1.0].index, 
         last_2M_data.Gold_MA_3[last_2M_data.positions == -1.0],
         'v', markersize=10, color='r', label='Sell')

plt.legend(['Gold', 'MA (3 days)', 'MA (6 days)', 'Buy', 'Sell'])
plt.title('Gold prices evolution and moving averages with buy/sell signals')
plt.show()


# In[ ]:




