# Ping Identity Cloud SRE Exercise

## 1. How to Build and Run Locally

```bash
docker build -t stock-app .
docker run -e SYMBOL=MSFT -e NDAYS=7 -e APIKEY=YOUR_API_KEY -p 8000:8000 stock-app
