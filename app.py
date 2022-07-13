import streamlit as st
from multiapp import MultiApp
import p1, p2, p3

def main():
    app = MultiApp()
    st.title("Quant Finance Projects")

    # st.markdown("""
    # # Multi-Page App
    # This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
    # """)

    # Add all your application here
    app.add_app("Equal Weight S&P Index 500 Fund", p1.app)
    app.add_app("Quantitative Momentum Investing Strategy", p2.app)
    app.add_app("Model", p3.app)
    
    app.run()
    # The main app


if __name__ == '__main__':
    main()