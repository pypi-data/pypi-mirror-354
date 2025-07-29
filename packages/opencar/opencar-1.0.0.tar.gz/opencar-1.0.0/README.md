# OpenCar

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](https://github.com/llamasearchai/opencar/actions)
[![Coverage](https://img.shields.io/badge/coverage-53%25-orange.svg)](https://codecov.io/gh/llamasearchai/opencar)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/llamasearchai/opencar)

**OpenCar** is a production-ready autonomous vehicle perception system that combines advanced computer vision, machine learning, and AI to provide real-time object detection, scene analysis, and safety recommendations for autonomous driving applications.

## Features

### Core Capabilities
- **Real-time Object Detection**: YOLO-based detection with 90%+ accuracy
- **AI-Powered Scene Analysis**: GPT-4 Vision integration for comprehensive scene understanding
- **Safety Assessment**: Real-time hazard detection and safety scoring
- **Multi-Modal Processing**: Support for images, video streams, and sensor data
- **Production-Ready API**: FastAPI-based REST API with OpenAPI documentation

### Advanced Features
- **Async Processing**: High-performance async inference engine
- **Batch Processing**: Efficient batch inference for multiple inputs
- **Caching & Optimization**: Redis-based caching and model optimization
- **Monitoring & Observability**: Prometheus metrics, Grafana dashboards, distributed tracing
- **Scalable Architecture**: Docker containerization with Kubernetes support

### Enterprise Features
- **Security**: JWT authentication, rate limiting, security headers
- **Reliability**: Health checks, circuit breakers, graceful degradation
- **Compliance**: GDPR-ready data handling, audit logging
- **Integration**: OpenAI API, custom model support, webhook notifications

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (for containerized deployment)
- CUDA-compatible GPU (optional, for accelerated inference)

### Installation

#### Option 1: pip install (Recommended)
```bash
pip install opencar
```

#### Option 2: From source
```bash
git clone https://github.com/llamasearchai/opencar.git
cd opencar
pip install -e .
```

#### Option 3: Docker
```bash
docker pull llamasearchai/opencar:latest
docker run -p 8000:8000 llamasearchai/opencar:latest
```

### Basic Usage

#### CLI Interface
```bash
# Initialize a new project
opencar init my-project

# Start the API server
opencar serve --host 0.0.0.0 --port 8000

# Check system status
opencar status

# View system information
opencar info
```

#### Python API
```python
import asyncio
from opencar.perception.models.detector import ObjectDetector
from opencar.integrations.openai_client import OpenAIClient

async def main():
    # Initialize detector
    detector = ObjectDetector()
    await detector.initialize()
    
    # Detect objects in image
    with open("street_scene.jpg", "rb") as f:
        image_data = f.read()
    
    detections = await detector.detect(image_data)
    print(f"Found {len(detections)} objects")
    
    # AI scene analysis
    client = OpenAIClient(api_key="your-api-key")
    analysis = await client.analyze_image(image_data, "safety")
    print(f"Safety score: {analysis['safety_score']}")

asyncio.run(main())
```

#### REST API
```bash
# Health check
curl http://localhost:8000/health

# Object detection
curl -X POST "http://localhost:8000/api/v1/perception/detect" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@street_scene.jpg"

# Scene analysis
curl -X POST "http://localhost:8000/api/v1/perception/analyze" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@street_scene.jpg" \
     -F "analysis_type=comprehensive"
```

## Documentation

### API Reference

#### Object Detection Endpoint
```http
POST /api/v1/perception/detect
Content-Type: multipart/form-data

Parameters:
- file: Image file (JPEG, PNG)
- confidence_threshold: float (0.0-1.0, default: 0.5)

Response:
{
  "request_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z",
  "detections": [
    {
      "class_name": "car",
      "confidence": 0.92,
      "bbox": {"x1": 100, "y1": 200, "x2": 300, "y2": 400},
      "attributes": {"vehicle_type": "sedan"}
    }
  ],
  "image_info": {
    "filename": "image.jpg",
    "size": 1024000,
    "content_type": "image/jpeg"
  }
}
```

#### Scene Analysis Endpoint
```http
POST /api/v1/perception/analyze
Content-Type: multipart/form-data

Parameters:
- file: Image file (JPEG, PNG)
- analysis_type: string (comprehensive|traffic|safety|weather|navigation)

Response:
{
  "request_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z",
  "analysis": {
    "scene_type": "urban",
    "objects": ["car", "person", "traffic_light"],
    "hazards": [],
    "recommendations": ["proceed_normally"],
    "safety_score": 0.85,
    "weather_conditions": "clear",
    "traffic_situation": "normal"
  },
  "confidence": 0.85,
  "analysis_type": "comprehensive"
}
```

### Configuration

#### Environment Variables
```bash
# Core settings
OPENCAR_ENV=production
OPENCAR_DEBUG=false
OPENCAR_LOG_LEVEL=INFO

# API settings
OPENCAR_API_HOST=0.0.0.0
OPENCAR_API_PORT=8000

# Database
OPENCAR_DATABASE_URL=postgresql://user:pass@localhost:5432/opencar

# Redis
OPENCAR_REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENCAR_OPENAI_API_KEY=your-api-key

# Monitoring
OPENCAR_SENTRY_DSN=your-sentry-dsn
```

#### Configuration File (opencar.yaml)
```yaml
project:
  name: my-opencar-project
  version: 1.0.0

perception:
  models:
    - yolov8n
    - yolov8s
  confidence_threshold: 0.5
  nms_threshold: 0.4
  max_detections: 100

inference:
  device: cuda  # or cpu
  batch_size: 4
  use_tensorrt: false
  use_onnx: false

api:
  cors_origins:
    - "http://localhost:3000"
    - "https://yourdomain.com"
  rate_limit: 100  # requests per minute
  max_file_size: 10485760  # 10MB

monitoring:
  enable_metrics: true
  enable_tracing: true
  log_requests: true
```

## 🐳 Docker Deployment

### Development
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f opencar-api

# Stop services
docker-compose down
```

### Production
```bash
# Build production image
docker build --target production -t opencar:latest .

# Start production stack
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale API instances
docker-compose up -d --scale opencar-api=3
```

### Kubernetes
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app=opencar

# View logs
kubectl logs -f deployment/opencar-api
```

## Development

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/opencar/opencar.git
cd opencar

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run with coverage
pytest --cov=opencar --cov-report=html

# Format code
black src/ tests/
ruff check src/ tests/

# Type checking
mypy src/
```

### Project Structure
```
opencar/
├── src/opencar/           # Main package
│   ├── api/              # FastAPI application
│   │   ├── routes/       # API endpoints
│   │   ├── middleware/   # Custom middleware
│   │   └── schemas/      # Pydantic models
│   ├── perception/       # Computer vision models
│   │   ├── models/       # Detection models
│   │   ├── processors/   # Image processors
│   │   └── utils/        # Utilities
│   ├── ml/              # Machine learning
│   │   ├── inference/    # Inference engine
│   │   ├── training/     # Training utilities
│   │   └── optimization/ # Model optimization
│   ├── integrations/    # External integrations
│   ├── config/          # Configuration
│   └── cli/             # Command-line interface
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── docker/             # Docker configurations
├── k8s/               # Kubernetes manifests
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

### Testing
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Run with markers
pytest -m "not slow"
pytest -m integration

# Generate coverage report
pytest --cov=opencar --cov-report=html
open htmlcov/index.html
```

### Performance Testing
```bash
# Benchmark inference
pytest --benchmark-only

# Load testing
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

## Monitoring & Observability

### Metrics (Prometheus)
- Request latency and throughput
- Model inference performance
- System resource usage
- Error rates and types

### Dashboards (Grafana)
- Real-time performance metrics
- System health overview
- Model accuracy tracking
- Business KPIs

### Logging (Structured)
- Request/response logging
- Error tracking with stack traces
- Performance profiling
- Audit trails

### Tracing (Jaeger)
- Distributed request tracing
- Performance bottleneck identification
- Service dependency mapping

## Security

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (RBAC)
- API key management
- OAuth2 integration

### Security Features
- Rate limiting and DDoS protection
- Input validation and sanitization
- Security headers (HSTS, CSP, etc.)
- Encrypted data transmission (TLS)

### Compliance
- GDPR-compliant data handling
- SOC 2 Type II controls
- Audit logging and monitoring
- Data retention policies

## Production Deployment

### Cloud Platforms

#### AWS
```bash
# Deploy with AWS ECS
aws ecs create-cluster --cluster-name opencar-cluster
aws ecs create-service --cluster opencar-cluster --service-name opencar-api

# Deploy with AWS EKS
eksctl create cluster --name opencar-cluster
kubectl apply -f k8s/aws/
```

#### Google Cloud
```bash
# Deploy with Google Cloud Run
gcloud run deploy opencar-api --image gcr.io/project/opencar:latest

# Deploy with GKE
gcloud container clusters create opencar-cluster
kubectl apply -f k8s/gcp/
```

#### Azure
```bash
# Deploy with Azure Container Instances
az container create --resource-group opencar-rg --name opencar-api

# Deploy with AKS
az aks create --resource-group opencar-rg --name opencar-cluster
kubectl apply -f k8s/azure/
```

### Performance Optimization
- Model quantization and pruning
- TensorRT optimization for NVIDIA GPUs
- ONNX runtime for cross-platform inference
- Batch processing for improved throughput

### Scaling Strategies
- Horizontal pod autoscaling (HPA)
- Vertical pod autoscaling (VPA)
- Cluster autoscaling
- Load balancing with session affinity

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Write comprehensive docstrings
- Maintain test coverage above 80%
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [YOLO](https://github.com/ultralytics/yolov5) for object detection models
- [OpenAI](https://openai.com/) for GPT-4 Vision API
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [Docker](https://www.docker.com/) for containerization

## Support

- Email: nikjois@llamasearch.ai
- Documentation: [GitHub README](https://github.com/llamasearchai/opencar#readme)
- Issues: [GitHub Issues](https://github.com/llamasearchai/opencar/issues)

---

**Made with love by the OpenCar Team** 