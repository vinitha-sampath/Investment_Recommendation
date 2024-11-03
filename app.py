import pandas as pd
import streamlit as st
import yfinance as yf
import os
import matplotlib.pyplot as plt
import requests

# Paths to your CSV and stock data for US and AUS
stock_prediction_csv_us = "C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\stock_prediction_US.csv"
stock_data_path_us = "C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\Stocks_data\\us\\"

stock_prediction_csv_aus = "C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\stock_prediction_AUS.csv"
stock_data_path_aus = "C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\Stocks_data\\aus\\"

gold_prediction_csv = "C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\gold_pred.csv"

html_file_path = "C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\Growth_Areas_Map.html"

# Streamlit app layout
st.title("Investment Recommendation System")

# Sidebar for navigation
st.sidebar.header("Navigation")
sidebar_option = st.sidebar.selectbox(
    "Choose an option", 
    ["Recommendations", "US Stock Recommendations", "AUS Stock Recommendations", "Gold Recommendations", "Real Estate Recommendations", "News", "How to Invest?", "About"]
)

# Define buy/sell/hold strategy function
def get_trade_signals(actual_prices, predicted_prices, buy_threshold=0.02, sell_threshold=0.02):
    signals = []
    for actual, predicted in zip(actual_prices, predicted_prices):
        if predicted > actual * (1 + buy_threshold):
            signals.append('Buy')
        elif predicted < actual * (1 - sell_threshold):
            signals.append('Sell')
        else:
            signals.append('Hold')
    return signals

# Function to display news for a given ticker
def display_ticker_news(ticker):
    st.subheader(f"Latest News for {ticker}")
    try:
        ticker_data = yf.Ticker(ticker)
        news = ticker_data.news
        if news:
            for article in news[:5]:  # Display up to 5 news articles
                st.write(f"**{article['title']}**")
                st.write(f"{article['publisher']} - {article['providerPublishTime']}")
                st.write(article['link'])
                st.write("\n")
        else:
            st.write("No recent news available.")
    except Exception as e:
        st.error(f"Error fetching news for {ticker}: {e}")
        
def fetch_economic_news():
    try:
        # Define a list of tickers relevant for economic news
        tickers = ['^DJI', '^GSPC', '^IXIC']  # Dow Jones, S&P 500, NASDAQ
        news = []

        for ticker in tickers:
            ticker_data = yf.Ticker(ticker)
            news.extend(ticker_data.news)

        if news:
            st.subheader("Latest Economic News")
            for article in news[:5]:  # Display up to 5 news articles
                st.write(f"**{article['title']}**")
                st.write(f"{article['publisher']} - {article['providerPublishTime']}")
                st.write(article['link'])
                st.write("\n")
        else:
            st.write("No recent economic news available.")
    except Exception as e:
        st.error(f"Error fetching economic news: {e}")

        
# Home
# Define the categories
age_groups = ['18-24', '25-49', '50-64', '65+']
occupations = ['Employee', 'Businessman', 'Other']
income_brackets = ['10,000-50,000', '50,001-70,000', '70,001-100,000', '100,001-150,000', '150,000+']
goal_times = ['2 years', '5 years', '10 years', '11+']
savings_options = ['Savings (30%)', 'Savings (20%)', 'Savings (10%)']
investment_options = ['Stocks', 'Gold', 'Real Estate']

# Function to determine investment recommendations based on economic factors
def analyze_investments(income_level, savings_level):
    investments = [0] * len(investment_options)
    recommendation = []

    # High income
    if income_level == 3:
        investments = [1, 1, 1]  # Stocks, Gold, Real Estate
        recommendation.append("Stocks, Gold, Real Estate")
    # Moderate income
    elif income_level == 2:
        if savings_level == 0:  # High savings (30%)
            investments = [1, 1, 1]  # Stocks, Gold, Real Estate
            recommendation.append("Stocks, Gold, Real Estate")
        elif savings_level == 1:  # Moderate savings (20%)
            investments = [1, 1, 0]  # Stocks, Gold
            recommendation.append("Stocks, Gold")
        elif savings_level == 2:  # Low savings (10%)
            investments = [1, 0, 0]  # Stocks only
            recommendation.append("Stocks")
    # Low income
    elif income_level == 1:
        if savings_level == 0:  # High savings (30%)
            investments = [1, 1, 0]  # Stocks, Gold
            recommendation.append("Stocks, Gold")
        elif savings_level in [1, 2]:  # Moderate or low savings
            investments = [1, 0, 0]  # Stocks only
            recommendation.append("Stocks")

    # Ensure a default recommendation if none apply
    if not recommendation:
        recommendation.append("Stocks")  # Default to stocks for broad applicability

    return investments, ", ".join(recommendation)

# Recommendations Section
if sidebar_option == "Recommendations":
    	# Display the image at the top
    st.image("C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\image.jpg", width=300)
    st.subheader("Personalized Investment Recommendations")

    # User input for recommendations
    st.write("Please provide your details below to receive tailored investment recommendations based on your profile:")
    age_group = st.selectbox("Select Age Group", age_groups)
    occupation = st.selectbox("Select Occupation", occupations)
    income_level = st.selectbox("Select Income Bracket", income_brackets)
    goal_time = st.selectbox("Select Goal Time", goal_times)
    savings_level = st.selectbox("Select Savings Level", savings_options)
    st.write("Based on your responses, we will provide personalized investment recommendations that align with your financial goals and situation.")
    st.write("Disclaimer: All contents discussed do not constitute investment advice")

    # Map user input to numerical values for analysis
    income_mapping = {
        '10,000-50,000': 1,
        '50,001-70,000': 2,
        '70,001-100,000': 2,
        '100,001-150,000': 3,
        '150,000+': 3
    }
    savings_mapping = {
        'Savings (30%)': 0,
        'Savings (20%)': 1,
        'Savings (10%)': 2
    }

    # Get numerical values for income and savings
    income_level_numeric = income_mapping[income_level]
    savings_level_numeric = savings_mapping[savings_level]

    # Button to get recommendations
    if st.button("Get Investment Recommendation"):
        investments, recommendation = analyze_investments(income_level_numeric, savings_level_numeric)
        st.write("Based on your input, we recommend the following investment options:")
        st.write(recommendation)

# US Stock Recommendations Section
if sidebar_option == "US Stock Recommendations":
    st.subheader("US Stock Recommendations")

    # User input for US stock ticker
    us_ticker = st.selectbox("Choose a US stock ticker:", [
        "AAPL", "NVDA", "MSFT", "GOOG", "AMZN", "META", "TSLA", "WMT", "JPM", "XOM", 
        "HD", "PG", "JNJ", "BAC", "KO", "NFLX", "AMD", "BABA", "MCD", "CSCO", "IBM", 
        "GE", "VZ", "DIS", "PFE", "T", "C", "INTC", "BA", "F"
    ])

    # Fetch and display live US ticker price
    try:
        live_data_us = yf.download(us_ticker, period="1d", interval="1m")
        if not live_data_us.empty and 'Close' in live_data_us.columns:
            live_price_us = float(live_data_us['Close'].iloc[-1])
            st.write(f"**Current Price of {us_ticker}: ${live_price_us:.2f}**")
        else:
            st.warning("No live price data available for US stocks. Please check the ticker symbol.")
    except Exception as e:
        st.error(f"Error fetching live price for {us_ticker}: {e}")

    # Load US stock prediction data
    if os.path.exists(stock_prediction_csv_us):
        stock_predictions_us = pd.read_csv(stock_prediction_csv_us)
        ticker_predictions_us = stock_predictions_us[stock_predictions_us['Ticker'] == us_ticker]

        if ticker_predictions_us.empty:
            st.error(f"No predictions found for {us_ticker}.")
        else:
            actual_prices_us = ticker_predictions_us['Actual Price'].values
            predicted_prices_us = ticker_predictions_us['Predicted Price'].values
            predicted_prices_us = list(predicted_prices_us) + [live_price_us]
            actual_prices_us = list(actual_prices_us) + [actual_prices_us[-1]]
            trade_signals_us = get_trade_signals(actual_prices_us, predicted_prices_us)
            last_signal_us = trade_signals_us[-1]
            st.write(f"**Current Price of {us_ticker}: ${live_price_us:.2f}. Recommended to {last_signal_us}.**")
            ticker_predictions_us['Trade Signal'] = trade_signals_us[:-1]
            st.write("US Stock Predictions Loaded:")

            historical_csv_path_us = os.path.join(stock_data_path_us, f"{us_ticker}.csv")
            if os.path.exists(historical_csv_path_us):
                historical_data_us = pd.read_csv(historical_csv_path_us)
                historical_data_us['Date'] = pd.to_datetime(historical_data_us['Date'])
                historical_data_us.set_index('Date', inplace=True)
                st.subheader(f"Closing Price for {us_ticker} (Last 15 Days)")
                st.line_chart(historical_data_us['Close'].tail(15))
                st.subheader(f"Volume for {us_ticker} (Last 15 Days)")
                st.line_chart(historical_data_us['Volume'].tail(15))
            else:
                st.error(f"Historical data file for {us_ticker} not found in {stock_data_path_us}.")

            # Display news for the US ticker
            display_ticker_news(us_ticker)

# AUS Stock Recommendations Section
elif sidebar_option == "AUS Stock Recommendations":
    st.subheader("AUS Stock Recommendations")

    # User input for AUS stock ticker
    aus_ticker = st.selectbox("Choose an AUS stock ticker:", [
        'CBA.AX', 'ANZ.AX', 'WBC.AX', 'NAB.AX', 'BHP.AX', 'CSL.AX', 'TLS.AX', 'WOW.AX', 'QBE.AX', 'RIO.AX'
    ])

    # Fetch and display live AUS ticker price
    try:
        live_data_aus = yf.download(aus_ticker, period="1d", interval="1m")  # Append '.AX' for ASX tickers
        if not live_data_aus.empty and 'Close' in live_data_aus.columns:
            live_price_aus = float(live_data_aus['Close'].iloc[-1])
            st.write(f"**Current Price of {aus_ticker}: ${live_price_aus:.2f}**")
        else:
            st.warning("No live price data available for AUS stocks. Please check the ticker symbol.")
    except Exception as e:
        st.error(f"Error fetching live price for {aus_ticker}: {e}")

    # Load AUS stock prediction data
    if os.path.exists(stock_prediction_csv_aus):
        stock_predictions_aus = pd.read_csv(stock_prediction_csv_aus)
        ticker_predictions_aus = stock_predictions_aus[stock_predictions_aus['Ticker'] == aus_ticker]

        if ticker_predictions_aus.empty:
            st.error(f"No predictions found for {aus_ticker}.")
        else:
            actual_prices_aus = ticker_predictions_aus['Actual Price'].values
            predicted_prices_aus = ticker_predictions_aus['Predicted Price'].values
            predicted_prices_aus = list(predicted_prices_aus) + [live_price_aus]
            actual_prices_aus = list(actual_prices_aus) + [actual_prices_aus[-1]]
            trade_signals_aus = get_trade_signals(actual_prices_aus, predicted_prices_aus)
            last_signal_aus = trade_signals_aus[-1]
            st.write(f"**Current Price of {aus_ticker}: ${live_price_aus:.2f}. Recommended to {last_signal_aus}.**")
            ticker_predictions_aus['Trade Signal'] = trade_signals_aus[:-1]
            st.write("AUS Stock Predictions Loaded:")

            historical_csv_path_aus = os.path.join(stock_data_path_aus, f"{aus_ticker}.csv")
            if os.path.exists(historical_csv_path_aus):
                historical_data_aus = pd.read_csv(historical_csv_path_aus)
                historical_data_aus['Date'] = pd.to_datetime(historical_data_aus['Date'])
                historical_data_aus.set_index('Date', inplace=True)
                st.subheader(f"Closing Price for {aus_ticker} (Last 15 Days)")
                st.line_chart(historical_data_aus['Close'].tail(15))
                st.subheader(f"Volume for {aus_ticker} (Last 15 Days)")
                st.line_chart(historical_data_aus['Volume'].tail(15))
            else:
                st.error(f"Historical data file for {aus_ticker} not found in {stock_data_path_aus}.")

            # Display news for the AUS ticker
            display_ticker_news(aus_ticker )

# Gold Recommendations Section
elif sidebar_option == "Gold Recommendations":
    st.subheader("Gold Price Forecast")
    try:
        # Fetch live gold price using GLD ETF as a proxy
        gold_ticker = 'GC=F'
        gold_data = yf.download(gold_ticker, period="1d", interval="1m")
        if not gold_data.empty and 'Close' in gold_data.columns:
            live_gold_price = float(gold_data['Close'].iloc[-1])
            st.write(f"**Current Price of Gold (GLD): ${live_gold_price:.2f}**")
        else:
            st.warning("No live gold price data available.")
    except Exception as e:
        st.error(f"Error fetching live gold price: {e}")

    # Load the gold predictions CSV file
    if os.path.exists(gold_prediction_csv):
        gold_predictions = pd.read_csv(gold_prediction_csv)

        actual_gold_price = gold_predictions['Actual Price'].iloc[-1]
        predicted_gold_price = gold_predictions['Predicted Price'].iloc[-1]
        gold_actual_prices = gold_predictions['Actual Price'].values
        gold_predicted_prices = list(gold_predictions['Predicted Price'].values) + [live_gold_price]
        gold_actual_prices = list(gold_actual_prices) + [actual_gold_price]
        gold_trade_signals = get_trade_signals(gold_actual_prices, gold_predicted_prices)

        last_gold_signal = gold_trade_signals[-1]
        # Moved this line above the predictions section
        st.write(f"**Current Gold Price: ${live_gold_price:.2f}. Recommended to {last_gold_signal}.**")


		        # Display news for gold
        display_ticker_news("GC=F")
    else:
        st.error("Gold prediction CSV file not found.")

# Real Estate Recommendations Section
if sidebar_option == "Real Estate Recommendations":
    st.subheader("Real Estate Investment Insights")
    
    # Provide insights about real estate investment
    st.write("""
    In the current economic landscape, real estate continues to be a promising avenue for investment, offering potential for both capital appreciation and rental income. 
             
    Investors should consider focusing on emerging markets, where property values are on the rise due to urbanization and infrastructural developments.
    """)

    # Display the HTML content for the map
    st.write("### Areas of Growth in NSW:")
    
    # Path to the HTML file
    html_file_path = "C:\\Users\\Vinitha\\Desktop\\Capstone_project\\Main\\Growth_Areas_Map.html"
    
    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            st.components.v1.html(html_content, height=600)  # Adjust height as necessary
    else:
        st.error("Growth Areas Map file not found.")
        
# News Section
elif sidebar_option == "News":
    fetch_economic_news()


# How to Invest Section
elif sidebar_option == "How to Invest?":
    st.subheader("Investment Guidance")
    st.write("### Before You Invest:")
    st.write("1. **Eliminate Debt**: Pay off loans and credit card balances.")
    st.write("2. **Emergency Fund**: Save three months' expenses to avoid selling investments.")

    st.write("### Preparing to Invest:")
    st.write("3. **Investment Plan**: Define your goals, risk tolerance, and timeline.")
    st.write("4. **Research Assets**: Understand risks and returns; higher returns mean higher risks.")
    st.write("5. **Know Your Investment**: Understand pros, cons, fees, and tax implications.")
    st.write("6. **Beware of Scams**: Verify bank details and use AFCA to check firms.")
    st.write("7. **Seek Advice**: Consult a financial adviser or discuss with trusted individuals.")
    st.write("8. **Diversify**: Spread investments across asset classes to reduce risk.")

    st.write("### Monitoring Investments:")
    st.write("9. **Track Your Portfolio**: Keep documentation and review investments regularly.")
    st.write("10. **Exit Strategy**: Know how to access funds and any withdrawal fees.")

    st.write("For more resources on investing, visit [MoneySmart](https://moneysmart.gov.au/).")
    
# About Section
elif sidebar_option == "About":
    st.subheader("About This App")
    st.write("This app provides investment recommendations and insights tailored to your financial goals. It includes:")
    
    st.write("- **Stock Recommendations**: Get personalized suggestions for US and AUS stocks based on market trends and analysis.")
    st.write("- **Gold Investment Insights**: Access real-time data and forecasts for gold prices.")
    st.write("- **Current News**: Stay updated with the latest economic news that can impact your investments.")
    st.write("- **User-Friendly Interface**: Navigate easily through different sections for a seamless experience.")
    
    st.write("Whether you're a beginner or an experienced investor, this app aims to empower you with the information you need to make informed investment decisions.")
    
    st.write("Developed by Vinitha Sampathkumar")
    st.write("Contact: info@investmentapp.com")
    st.write("Disclaimer: All contents discussed do not constitute investment advice")

