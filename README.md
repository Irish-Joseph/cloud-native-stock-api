# Cloud Native Stock API

## 📊 Project Description

This is a **Cloud-Native Stock Market API** I built to demonstrate modern microservices architecture and cloud-native development practices. The service provides a RESTful API that fetches real-time stock market data and performs financial calculations.

### What it does:
- 🔍 **Fetches stock data** from Alpha Vantage API for any stock symbol
- 📈 **Calculates average closing prices** over a configurable number of days
- 🌐 **Serves JSON API** with stock prices and calculated averages
- 🐳 **Containerized** for consistent deployment across environments
- ☸️ **Kubernetes-ready** with production-grade manifests

### Architecture:
```
Internet → Ingress → Service → Deployment (Pod) → Alpha Vantage API
                                     ↓
                               ConfigMap & Secret
```

## ⚡ Quick Start

### Option 1: Docker (Recommended for testing)
```bash
# 1. Clone the repository  
git clone https://github.com/Irish-Joseph/cloud-native-stock-api.git
cd cloud-native-stock-api

# 2. Build and run with Docker
docker build -t stock-app .
docker run -e SYMBOL=AAPL -e NDAYS=5 -e APIKEY=demo -p 8000:8000 stock-app

# 3. Test the API
curl http://localhost:8000/
```

### Option 2: Kubernetes (Production deployment)
```bash
# 1. Deploy to your K8s cluster  
kubectl apply -f k8s/

# 2. Check deployment status
kubectl get pods,svc

# 3. Access the service
kubectl port-forward service/stock-service 8080:80
curl http://localhost:8080/
```

## 🛠️ Features

- ✅ Real-time stock price fetching
- ✅ Configurable stock symbols and time periods
- ✅ Average price calculations
- ✅ Health check endpoints
- ✅ Error handling and validation
- ✅ Resource limits and monitoring probes
- ✅ Production-ready Kubernetes manifests

## Prerequisites

- Docker
- Kubernetes cluster (for K8s deployment)
- Alpha Vantage API key (get free at: https://www.alphavantage.co/support/#api-key)

## 1. Build and Run Locally

### Using Docker Compose (Recommended)
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your API key

# Run with docker-compose
docker-compose up --build
```

### Using Docker directly
```bash
# Build the image
docker build -t stock-app .

# Run with environment variables
docker run -e SYMBOL=MSFT -e NDAYS=7 -e APIKEY=YOUR_API_KEY -p 8000:8000 stock-app
```

### Using Python directly
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables and run
export SYMBOL=MSFT
export NDAYS=7
export APIKEY=YOUR_API_KEY
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 2. Kubernetes Deployment

### Prerequisites
- Kubernetes cluster running
- kubectl configured

### Deploy to Kubernetes
```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

### Configuration
- **ConfigMap** (`k8s/configmap.yaml`): Contains SYMBOL and NDAYS configuration
- **Secret** (`k8s/secret.yaml`): Contains API key (base64 encoded)
- **Deployment** (`k8s/deployment.yaml`): Main application deployment
- **Service** (`k8s/service.yaml`): Internal service exposure
- **Ingress** (`k8s/ingress.yaml`): External access configuration

## 3. API Usage

Once running, access the API at:
- Local: `http://localhost:8000/`
- Kubernetes: `http://<cluster-ip>/` or via ingress

### Response Format
```json
{
  "symbol": "MSFT",
  "average_close": 420.15,
  "data": [
    {
      "date": "2024-11-01",
      "close": 425.30
    },
    {
      "date": "2024-10-31", 
      "close": 415.00
    }
  ]
}
```

## 4. Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| SYMBOL | Stock symbol to fetch | MSFT | No |
| NDAYS | Number of days for average | 7 | No |
| APIKEY | Alpha Vantage API key | - | Yes |

## 5. Resilience Considerations

For production deployment, consider:
- **Health checks**: Add `/health` endpoint
- **Resource limits**: Set CPU/memory limits in deployment
- **Horizontal Pod Autoscaler**: Auto-scale based on load
- **Circuit breaker**: Handle API failures gracefully
- **Monitoring**: Add prometheus metrics
- **Logging**: Structured logging with correlation IDs
- **Rate limiting**: Respect Alpha Vantage API limits
- **Caching**: Cache API responses to reduce external calls

## 6. Testing & Validation

### Automated Testing
```bash
# Run the test script
python test_api.py

# Or test manually
curl http://localhost:8000/
curl http://localhost:8000/health
```

### Local Testing
```bash
# Test with different parameters
curl "http://localhost:8000/?symbol=GOOGL"

# Using Docker Compose
docker-compose up -d
python test_api.py
docker-compose down
```

### Kubernetes Testing
```bash
# Test in Kubernetes
kubectl port-forward service/stock-service 8080:80
curl http://localhost:8080/

# Check pod logs
kubectl logs -l app=stock-app

# Check configuration
kubectl get configmap stock-config -o yaml
kubectl get secret stock-secret -o yaml
```

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| `API key not configured` | Set the APIKEY environment variable |
| `No data found for symbol` | Check if the stock symbol is valid |
| `API rate limit exceeded` | Wait or use a premium Alpha Vantage key |
| Pod not starting | Check `kubectl describe pod <pod-name>` |
| Service not accessible | Verify service and ingress configuration |

## 📁 Project Structure

```
cloud-native-stock-api/
├── app.py                # Main FastAPI application
├── requirements.txt      # Python dependencies  
├── Dockerfile           # Container build instructions
├── docker-compose.yml   # Local development setup
├── test_api.py         # API testing script
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
├── k8s/               # Kubernetes manifests
│   ├── configmap.yaml    # Environment configuration
│   ├── secret.yaml       # API key storage
│   ├── deployment.yaml   # Application deployment  
│   ├── service.yaml      # Internal service
│   └── ingress.yaml      # External access
└── README.md          # Project documentation
```

## 🔧 Development Notes

- Built with **FastAPI** for high performance and automatic API docs
- Uses **Alpha Vantage** free tier (5 API calls per minute, 500 per day)
- Designed following **12-factor app** principles
- Implements **health checks** and **graceful error handling**
- Production-ready with **resource limits** and **monitoring probes**

## 📊 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

## 🚀 Future Enhancements

Ideas for extending this project:
- Add caching layer (Redis) for API responses
- Implement WebSocket for real-time stock updates  
- Add user authentication and personalized watchlists
- Include technical indicators (RSI, MACD, etc.)
- Add historical data visualization charts
- Implement alerting system for price thresholds

## 🤝 Contributing

This is a personal project, but feel free to:
- Report issues or bugs
- Suggest new features
- Submit pull requests for improvements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## Author

** Irish Joseph** - Full Stack Developer & DevOps Enthusiast

📧 Contact: []  
🔗 LinkedIn: []  
🐙 GitHub: [@Irish-Joseph](https://github.com/Irish-Joseph)

---
*This project showcases modern cloud-native development practices including containerization, Kubernetes orchestration, API development, and SRE principles.*