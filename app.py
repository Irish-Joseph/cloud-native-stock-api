# app.py

import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

SYMBOL = os.getenv("SYMBOL", "MSFT")
NDAYS = int(os.getenv("NDAYS", 7))
APIKEY = os.getenv("APIKEY")

class StockData(BaseModel):
    date: str
    close: float

@app.get("/")
def get_stock_data():
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "apikey": APIKEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    time_series = data.get("Time Series (Daily)", {})
    
    dates = sorted(time_series.keys(), reverse=True)[:NDAYS]
    
    stocks = []
    total_close = 0.0
    
    for date in dates:
        close_price = float(time_series[date]["4. close"])
        stocks.append(StockData(date=date, close=close_price))
        total_close += close_price
    
    average_close = total_close / NDAYS if NDAYS else 0

    return {
        "symbol": SYMBOL,
        "average_close": average_close,
        "data": [s.dict() for s in stocks]
    }
