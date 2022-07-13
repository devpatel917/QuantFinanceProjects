import streamlit as st
import pandas as pd
import requests
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'

def portfolio(value):
    #1 Load S&P 500 Index Stocks
    stocks = pd.read_csv('sp_500_stocks.csv')
    stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC','VIAC','WLTW'])]

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    my_columns = ['Ticker', 'Price','Market Capitalization', 'Number Of Shares to Buy']
    final_dataframe = pd.DataFrame(columns = my_columns)

    #2. Split Stocks into batches
    symbol_groups = list(chunks(stocks['Ticker'], 100))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))

    #3. Batch API call (for each batch)
    for symbol_string in symbol_strings:
        #     print(symbol_strings)
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            final_dataframe.loc[len(final_dataframe.index)] = [symbol, data[symbol]['quote']['latestPrice'], data[symbol]['quote']['marketCap'], 'N/A'] 
    
    #4. Calculate Number of Shares to Buy (each stock has equal weight)
    portfolio_size = value
    position_size = float(portfolio_size) / len(final_dataframe.index)
    for i in range(0, len(final_dataframe['Ticker'])):
        final_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size / final_dataframe['Price'][i])

    return final_dataframe
    
def func(x, a, b, c):
      #return a * np.exp(-b * x) + c
  return a * np.log(b * x) + c

def app():
    st.title('Equal Weight S&P Index 500 Fund')
    st.subheader('Enter the value of your portfolio')

    with st.form(key='form1'):
        value = st.text_input('Portfolio Value (enter in US dollars)')
        submit_button = st.form_submit_button(label = "Submit")
    if submit_button:
        
        df = portfolio(value)
        fig = plt.figure()
        # ax = fig.add_subplot(1,1,1)

        plt.scatter(df["Price"], df["Number Of Shares to Buy"])
        plt.title("Number of Shares for each S&P 500 Stock")
        plt.xlabel("Stock Price")
        plt.ylabel("Number of Shares to Buy")
        st.write(fig)
        # df.style.set_properties(subset=['Number Of Shares to Buy'], **{'width': '500px'})
        st.table(df)
        
        # st.dataframe(df, width = 1800, height = 500)
        

    # st.write("This is the `Data` page of the multi-page app.")

    # st.write("The following is the DataFrame of the `iris` dataset.")