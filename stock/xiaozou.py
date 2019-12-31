#!/usr/bin/env python
# coding: utf-8

# In[2]:

import tushare as ts

# In[4]:


import pandas as pd
import numpy as np

# In[5]:


import warnings

warnings.simplefilter('ignore')
import matplotlib.pylab as plt
from IPython import get_ipython

get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.pylab import rcParams

rcParams['figure.figsize'] = 15, 8

# In[6]:


from datetime import date

# ## 获取国内股票中国联通（600050）的数据,计算收益率

# In[7]:


StockPrice = pd.DataFrame()
start = date(2018, 9, 30)
end = date(2019, 9, 30)
data = ts.get_hist_data('600050', start="2018-9-30", end="2019-9-30").sort_index()
StockPrice1 = data['close']
Stock_return = StockPrice1.pct_change().dropna()

Stock_return.tail()

# ## 进行平稳性检验

# In[8]:


from statsmodels.tsa.stattools import adfuller

# In[9]:


adfuller(Stock_return)


# #### 结果显著，拒绝该序列为非平稳性序列的假设。即该序列为平稳性序列

# In[10]:


def mplot(ts, loc=0, tit=''):
    ts.dropna(inplace=True)
    RB = pd.Series.rolling(ts, window=8).mean()
    RS = pd.Series.rolling(ts, window=8).std()
    plt.plot(ts, label='The series')
    plt.plot(RB, 'r-', label='The rolling mean')
    plt.plot(RS, 'b-', label='The rolling std')
    plt.title(tit)
    plt.legend(loc=loc)


# In[11]:


mplot(Stock_return, 2, 'Chinaunion1')

# ## 减去滑动平均

# In[12]:


Stock_return_rm = pd.Series.rolling(Stock_return, 5).mean()
Stock_returnR = Stock_return_rm - Stock_return
mplot(Stock_returnR, 2, "Chinaunion2")

# In[13]:


adfuller(Stock_returnR)

# #### 结果显著，减去移动平均后的序列为平稳性序列

# ## 序列差分

# In[14]:


Stock_return_shift = Stock_return.shift()
pd.concat([Stock_return, Stock_return_shift], axis=1).head()

# In[15]:


Stock_return_diff = Stock_return_shift - Stock_return
Stock_return_RM = pd.Series.rolling(Stock_return_diff, 5).mean()
Stock_returnD = Stock_return_diff - Stock_return_RM
mplot(Stock_returnD, 3, 'Chinaunion3')

# In[16]:


adfuller(Stock_returnD)

# #### 一阶差分后该序列为平稳序列

# ## ARMA模型的拟合和预测

# In[20]:


from statsmodels.tsa.stattools import acf, pacf


def ACF_PACF(ts, lag=20):
    lag_acf = acf(ts, nlags=lag)
    lag_pacf = pacf(ts, nlags=lag, method='ols')
    # 画 ACF:
    plt.subplot(121)
    plt.vlines(range(lag), [0], lag_acf, linewidth=5.0)
    plt.plot(lag_acf)
    plt.axhline(y=0, linestyle=':', color='blue')
    plt.axhline(y=-1.96 / np.sqrt(len(ts)), linestyle='--', color='red')
    plt.axhline(y=1.96 / np.sqrt(len(ts)), linestyle='--', color='red')
    plt.title('Autocorrelation Function')
    # 画 PACF:
    plt.subplot(122)
    plt.vlines(range(lag), [0], lag_pacf, linewidth=5.0)
    plt.plot(lag_pacf)
    plt.axhline(y=0, linestyle=':', color='blue')
    plt.axhline(y=-1.96 / np.sqrt(len(ts)), linestyle='--', color='red')
    plt.axhline(y=1.96 / np.sqrt(len(ts)), linestyle='--', color='red')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()


# In[18]:


ACF_PACF(Stock_returnD)

# ## ARMA拟合

# In[21]:


from statsmodels.tsa.arima_model import ARMA

SR_10_5 = ARMA(Stock_return, (10, 5)).fit()
print(SR_10_5.params)

# In[22]:


plt.plot(SR_10_5.resid)

# In[23]:


ACF_PACF(SR_10_5.resid)

# In[24]:

print("----------------------分割线24--------------------------")

from scipy import stats

stats.normaltest(SR_10_5.resid)

# #### 结果显著，该序列的残差项序列平稳

# ## Ljung-Box 自相关检验

# In[25]:

print("----------------------分割线25--------------------------")
# LB检验
import statsmodels.api as sm

r, q, p = sm.tsa.acf(SR_10_5.resid.values.squeeze(), qstat=True)
dt = np.c_[range(1, len(q) + 1), r[1:], q, p]
table = pd.DataFrame(dt, columns=['lag', 'AC', 'Q', 'Prob(>Q)'])
# print(table.set_index('lag'))
plt.plot(p, 'o')
plt.axhline(y=0, linestyle=':', color='blue')
plt.xlabel('lag')
plt.ylabel('p-value')
plt.title("Ljung-Box Test's p-value")

# In[26]:

print("----------------------分割线26--------------------------")

pred_SR = SR_10_5.predict(start='2019-03-01', end='2019-03-29')
plt.plot(Stock_return['2018-09-30':], label='Stock_return')
plt.plot(pred_SR, 'r--', label='Prediction', linewidth=5)
plt.legend(loc='best')

# In[ ]:
