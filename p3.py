import streamlit as st
import numpy as np
from scipy.stats import norm
import scipy.stats as stats
import matplotlib.pyplot as plt

def black_scholes(S, K, r, t, v):
    d1 = (np.log(S/K) + ((r + (v**2/2))*t))/(v*t**0.5)
    d2 = d1 - (v * t**0.5)

    exercise = S*norm.cdf(d1)

    present = K*np.e**(-r*t)*norm.cdf(d2)

    c = exercise - present
    return c

def monte_carlo(S, K, r, T, vol, N, M, market_value):
    #Precompute Constants
    dt = T/N
    nudt = (r - 0.5*vol**2)*dt
    volsdt = vol*np.sqrt(dt)
    lnS = np.log(S)


    # Monte Carlo Method
    Z = np.random.normal(size=(N, M)) 
    delta_lnSt = nudt + volsdt*Z 
    lnSt = lnS + np.cumsum(delta_lnSt, axis=0)
    lnSt = np.concatenate( (np.full(shape=(1, M), fill_value=lnS), lnSt ) )


    # Compute Expectation and SE
    ST = np.exp(lnSt)
    CT = np.maximum(0, ST - K)
    C0 = np.exp(-r*T)*np.sum(CT[-1])/M
    sigma = np.sqrt( np.sum( (CT[-1] - C0)**2) / (M-1) )
    SE = sigma/np.sqrt(M)

    st.write("Call value is ${0} with SE +/- {1}".format(np.round(C0,2),np.round(SE,2)))

    #Graph Distribution
    x1 = np.linspace(C0-3*SE, C0-1*SE, 100)
    x2 = np.linspace(C0-1*SE, C0+1*SE, 100)
    x3 = np.linspace(C0+1*SE, C0+3*SE, 100)
    s1 = stats.norm.pdf(x1, C0, SE)
    s2 = stats.norm.pdf(x2, C0, SE)
    s3 = stats.norm.pdf(x3, C0, SE)
    fig = plt.gcf()
    fig.set_size_inches(12, 8)
    plt.fill_between(x1, s1, color='tab:blue',label='> StDev')
    plt.fill_between(x2, s2, color='cornflowerblue',label='1 StDev')
    plt.fill_between(x3, s3, color='tab:blue')
    plt.plot([C0,C0],[0, max(s2)*1.1], 'k',
        label='Theoretical Value')
    plt.plot([market_value,market_value],[0, max(s2)*1.1], 'r',
        label='Market Value')
    plt.ylabel("Probability", fontsize = 16)
    plt.xlabel("Option Price", fontsize = 16)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.legend()
    plt.show()

    st.pyplot(fig)







def app():
    st.title('Option Pricing Models')

    with st.form(key='form1'):
        S = st.number_input(label = "Current Price of Asset", step = 1., format = "%.2f")
        K = st.number_input(label = "Strike Price", step = 1., format = "%.2f")
        r = st.number_input(label = "Risk-free Interest Rate", step = 1., format = "%.2f")
        t = st.number_input(label = "Time to Expiration (in years)", step = 1., format = "%.2f")
        v = st.number_input(label = "Volatility of Asset", step = 1., format = "%.2f")

        sts = st.number_input(label = "Number of time steps", step = 1)
        ns = st.number_input(label = "Number of Simulations", step = 1)
        mp = st.number_input(label = "Market Price (optional)", step = 1., format = "%.2f")




        submit_button = st.form_submit_button(label = "Calculate Option Price")
    if submit_button:
        option_price = black_scholes(S, K, r, t, v)
        st.write("Option Price (by Black Scholes Formula): ", option_price)
        st.write("Now using Monte Carlo...")
        monte_carlo(S, K, r, t, v, sts, ns, mp)

        


    