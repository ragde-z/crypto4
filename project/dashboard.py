# dashboard.py
import streamlit as st
import data_collection
import indicators
import model_predictions
import backtesting
import pandas as pd
import time

# Dashboard title
st.title("Crypto Analysis Dashboard")

# Sidebar for user inputs
st.sidebar.header("Data Collection")
symbol = st.sidebar.selectbox("Select Cryptocurrency Pair", ["BTCUSDT", "ETHUSDT", "BNBUSDT"])
interval = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"])

# Fetch historical data
st.header("Historical Data")
df = data_collection.get_data(symbol=symbol, interval=interval, limit=500)
st.write(df.tail())  # Display last few rows of data

# Calculate indicators
st.header("Indicators")
df['SMA_20'] = indicators.calculate_sma(df, window=20)
df['RSI'] = indicators.calculate_rsi(df)
df['MACD'] = indicators.calculate_macd(df)

# Display indicators
st.line_chart(df[['Close', 'SMA_20']])
st.line_chart(df['RSI'])
st.line_chart(df['MACD'])

# Model Predictions
st.header("Model Predictions")
df, model = model_predictions.train_model(df)
st.write(df[['Close', 'Prediction']].tail())

# Real-Time Backtesting
st.header("Real-Time Backtesting")

# Initialize metrics and position if not already present in the data
if 'Position' not in df.columns:
    df['Position'] = 0  # 0 = no trade, 1 = in a trade
    df['Entry Price'] = None
    df['Exit Price'] = None

# Initialize backtest metrics
metrics = backtesting.initialize_backtest(initial_balance=10000)

# Run the real-time backtest
metrics, df = backtesting.run_real_time_backtest(df, model, metrics)

# Display cumulative performance metrics
st.write("Total Return: {:.2f}%".format(metrics['total_return']))
st.write("Win Rate: {:.2f}%".format(metrics['win_rate'] * 100))
st.write("Number of Trades:", metrics['num_trades'])
st.write("Final Balance: ${:.2f}".format(metrics['balance']))

# Real-Time Prediction Section
st.header("Real-Time Prediction")
live_data = data_collection.fetch_live_data(symbol=symbol, interval="1m", lookback=20)

# Calculate indicators on live data
live_data['SMA_20'] = indicators.calculate_sma(live_data, window=20)
live_data['RSI'] = indicators.calculate_rsi(live_data)
live_data['MACD'] = indicators.calculate_macd(live_data)

# Prepare the latest features for prediction with the correct feature names
latest_features = pd.DataFrame([live_data[['SMA_20', 'RSI', 'MACD']].iloc[-1].values], 
                               columns=['SMA_20', 'RSI', 'MACD'])

# Make a prediction
latest_prediction = model.predict(latest_features)

# Display prediction
st.write("Next Movement Prediction:", "Up" if latest_prediction == 1 else "Down")

# Refresh every minute
time.sleep(60)
st.experimental_rerun()
