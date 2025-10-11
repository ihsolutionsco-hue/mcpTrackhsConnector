# Deployment Guide

## Production Deployment

This guide covers deploying the TrackHS MCP Connector to production environments.

## Prerequisites

- Python 3.8+ runtime
- Track HS API credentials
- Network access to Track HS API
- Environment variable configuration

## Environment Configuration

### Required Variables

```bash
# API Configuration
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=your_real_username
TRACKHS_PASSWORD=your_real_password
TRACKHS_TIMEOUT=30

# Production Settings
PRODUCTION=true
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### Security Considerations

- **Never commit credentials** to version control
- Use environment variables for all sensitive data
- Rotate credentials regularly
- Monitor access logs

## Platform-Specific Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY .env.example .env

ENV TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
ENV TRACKHS_USERNAME=your_username
ENV TRACKHS_PASSWORD=your_password

CMD ["python", "-m", "src.trackhs_mcp"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trackhs-mcp-connector
spec:
  replicas: 3
  selector:
    matchLabels:
      app: trackhs-mcp-connector
  template:
    metadata:
      labels:
        app: trackhs-mcp-connector
    spec:
      containers:
      - name: mcp-connector
        image: trackhs-mcp-connector:latest
        env:
        - name: TRACKHS_API_URL
          value: "https://ihmvacations.trackhs.com/api"
        - name: TRACKHS_USERNAME
          valueFrom:
            secretKeyRef:
              name: trackhs-secrets
              key: username
        - name: TRACKHS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: trackhs-secrets
              key: password
```

### Heroku

```bash
# Set environment variables
heroku config:set TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
heroku config:set TRACKHS_USERNAME=your_username
heroku config:set TRACKHS_PASSWORD=your_password

# Deploy
git push heroku main
```

## Monitoring & Logging

### Health Checks

```bash
# Check server status
curl http://localhost:8000/health

# Check API connectivity
python -c "
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
config = TrackHSConfig.from_env()
client = TrackHSApiClient(config)
print('API connectivity:', client.test_connection())
"
```

### Logging Configuration

```python
# Configure structured logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Troubleshooting

### Common Issues

#### "Endpoint not found"
- **Cause**: Environment variables not configured
- **Solution**: Verify all required environment variables are set

#### "Invalid credentials"
- **Cause**: Expired or incorrect credentials
- **Solution**: Update credentials and verify API access

#### "Connection timeout"
- **Cause**: Network connectivity issues
- **Solution**: Check firewall settings and network connectivity

### Diagnostic Scripts

```bash
# Test configuration
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API URL:', os.getenv('TRACKHS_API_URL'))
print('Username:', os.getenv('TRACKHS_USERNAME'))
print('Password set:', bool(os.getenv('TRACKHS_PASSWORD')))
"

# Test API connectivity
python -c "
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
try:
    config = TrackHSConfig.from_env()
    client = TrackHSApiClient(config)
    print('API connection successful')
except Exception as e:
    print('API connection failed:', e)
"
```

## Security Best Practices

1. **Environment Variables**: Use environment variables for all sensitive data
2. **Credential Rotation**: Rotate API credentials regularly
3. **Network Security**: Use HTTPS for all API communications
4. **Access Monitoring**: Monitor and log all API access
5. **Error Handling**: Implement proper error handling and logging

## Performance Optimization

### Resource Limits

```yaml
# Kubernetes resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Scaling

- **Horizontal Scaling**: Deploy multiple instances behind a load balancer
- **Vertical Scaling**: Increase memory and CPU resources
- **Caching**: Implement caching for frequently accessed data

## Backup & Recovery

### Configuration Backup

```bash
# Backup environment configuration
cp .env .env.backup
```

### Disaster Recovery

1. **Documentation**: Maintain up-to-date deployment documentation
2. **Backup**: Regular backup of configuration and data
3. **Testing**: Regular testing of recovery procedures
4. **Monitoring**: Continuous monitoring of system health

## Support

For deployment issues:

1. Check the logs for error messages
2. Verify environment variable configuration
3. Test API connectivity
4. Review security settings
5. Contact support with detailed error information
