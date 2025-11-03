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

@app.get("/health")
def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {"status": "healthy", "service": "stock-ticker"}

@app.get("/")
def get_stock_data():
    if not APIKEY:
        return {"error": "API key not configured"}
    
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "apikey": APIKEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            return {"error": f"API Error: {data['Error Message']}"}
        
        if "Note" in data:
            return {"error": "API rate limit exceeded. Please try again later."}
        
        time_series = data.get("Time Series (Daily)", {})
        
        if not time_series:
            return {"error": f"No data found for symbol: {SYMBOL}"}
            
    except requests.RequestException as e:
        return {"error": f"Failed to fetch data: {str(e)}"}
    
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
