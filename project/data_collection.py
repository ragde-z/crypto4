# data_collection.py
from binance.client import Client
import pandas as pd

# Replace these with your Binance.US API Key and Secret
api_key = "kP4f7oiIRaUju95QahyhYUOdFSBkVZTlIOQ4WE61bRwPXWFVrTGnH4NnSVZAWQEn"
api_secret = "WYB0uI9WtyOqzJofO28IGFTmoeiCNfU1aAm952is7dPR0kRHGAj9yzGv7UzFc5o1"

client = Client(api_key, api_secret, tld='us')

def get_data(symbol="BTCUSDT", interval="1h", limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
        'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
        'Taker Buy Quote Asset Volume', 'Ignore'
    ])
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close'] = df['Close'].astype(float)
    return df

import time

def fetch_live_data(symbol="BTCUSDT", interval="1m", lookback=20):
    # Fetch the latest data from Binance with a 20-minute lookback
    klines = client.get_klines(symbol=symbol, interval=interval, limit=lookback)
    df = pd.DataFrame(klines, columns=[
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
        'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
        'Taker Buy Quote Asset Volume', 'Ignore'
    ])
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close'] = df['Close'].astype(float)
    return df
