from binance.client import Client
import pandas as pd

# Your Binance.US API Key and Secret
api_key = "kP4f7oiIRaUju95QahyhYUOdFSBkVZTlIOQ4WE61bRwPXWFVrTGnH4NnSVZAWQEn"
api_secret = "WYB0uI9WtyOqzJofO28IGFTmoeiCNfU1aAm952is7dPR0kRHGAj9yzGv7UzFc5o1"

# Initialize Binance.US client by specifying the base URL for Binance.US
client = Client(api_key, api_secret, tld='us')  # 'tld' parameter specifies 'us' for Binance.US

try:
    # Fetch historical data for a specific cryptocurrency pair (e.g., BTCUSDT)
    klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=10)
    
    if klines:
        print("Data fetched successfully")
    else:
        print("No data received")
    
    # Convert data to a pandas DataFrame for easier handling
    df = pd.DataFrame(klines, columns=[
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 
        'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 
        'Taker Buy Quote Asset Volume', 'Ignore'
    ])

    # Display the first few rows of the data
    print(df.head())

except Exception as e:
    print("An error occurred:", e)
