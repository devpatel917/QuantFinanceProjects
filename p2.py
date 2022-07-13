import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt


def portfolio(value):
    df = pd.read_csv("hqm_dataframe.csv")

    portfolio_size = value
    position_size = float(portfolio_size) / len(df.index)
    for i in range(0, len(df['Ticker'])):
        df.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / df['Price'][i])
    return df
    


def app():
    st.title('Quantitative Momentum Investing Strategy')
    st.subheader('Enter the value of your portfolio')


    with st.form(key='form1'):
        value = st.text_input('Portfolio Value (enter in US dollars)')
        submit_button = st.form_submit_button(label = "Submit")
    if submit_button:
        
        df = portfolio(value)
        new_df = df.head(n = 10)
        # new_df = pd.DataFrame().assign(Ticker = new_df["Ticker"], Shares = new_df["Number of Shares to Buy"])
        # st.bar_chart(new_df)

        fig= plt.figure()
        plt.title('Top 10 Stocks (HQM Score)')
        plt.xlabel('Stocks')
        plt.ylabel('Number of Shares to Buy')
        # ax = fig.add_subplot(1,1,1)

        ticker = new_df["Ticker"]
        shares = new_df["Number of Shares to Buy"]
        plt.bar(ticker,shares)
        # plt.xlabel("Stocks")
        # plt.ylabel("Number of Shares to Buy")
    
        


        
        st.write(fig)
        # # fig = plt.figure()
        # # # ax = fig.add_subplot(1,1,1)

        # # plt.scatter(df["Price"], df["Number Of Shares to Buy"])
        # # plt.title("Number of Shares for each S&P 500 Stock")
        # # plt.xlabel("Stock Price")
        # # plt.ylabel("Number of Shares to Buy")
        # st.write(fig)
        # # df.style.set_properties(subset=['Number Of Shares to Buy'], **{'width': '500px'})
        st.table(df)



    