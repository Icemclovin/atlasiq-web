# 🐳 AtlasIQ Docker Deployment Guide

Complete guide for running AtlasIQ in Docker containers.

## 📋 Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0 or higher
- **Minimum 2GB RAM** available for containers
- **Ports 80 and 8000** available

## 🚀 Quick Start

### 1. Build and Start Containers

```powershell
# Navigate to project directory
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web

# Build and start all services
docker-compose -f docker-compose.prod.yml up --build -d
```

### 2. Check Container Status

```powershell
# View running containers
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. Access the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Default Admin Account

The initialization script creates an admin account:

- **Email**: `admin@atlasiq.com`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change this password immediately after first login!

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# JWT Secret (CHANGE THIS!)
JWT_SECRET_KEY=your-super-secret-random-key-here

# Admin Account (customize if needed)
ADMIN_EMAIL=admin@atlasiq.com
ADMIN_PASSWORD=admin123
ADMIN_NAME=Administrator

# Application
APP_ENV=production
DEBUG=false
```

### Generate Secure JWT Secret

```powershell
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})

# Or use Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📦 Docker Services

### Backend Service
- **Image**: Custom Python 3.11 image
- **Port**: 8000
- **Database**: SQLite (persisted in Docker volume)
- **Health Check**: Every 30s on `/health` endpoint

### Frontend Service
- **Image**: Nginx Alpine with React build
- **Port**: 80 (HTTP)
- **Features**: 
  - Production optimized build
  - Gzip compression
  - API proxy to backend
  - React Router support

## 🛠️ Management Commands

### Start Services
```powershell
docker-compose -f docker-compose.prod.yml up -d
```

### Stop Services
```powershell
docker-compose -f docker-compose.prod.yml down
```

### Restart Services
```powershell
docker-compose -f docker-compose.prod.yml restart
```

### View Logs
```powershell
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Rebuild After Code Changes
```powershell
# Rebuild all
docker-compose -f docker-compose.prod.yml up --build -d

# Rebuild specific service
docker-compose -f docker-compose.prod.yml up --build -d backend
```

## 💾 Data Persistence

### Database Volume

The SQLite database is stored in a Docker volume: `backend-data`

```powershell
# Inspect volume
docker volume inspect atlasiq-web_backend-data

# Backup database
docker run --rm -v atlasiq-web_backend-data:/data -v ${PWD}:/backup alpine tar czf /backup/atlasiq-backup.tar.gz -C /data .

# Restore database
docker run --rm -v atlasiq-web_backend-data:/data -v ${PWD}:/backup alpine tar xzf /backup/atlasiq-backup.tar.gz -C /data
```

## 🔍 Troubleshooting

### Container Won't Start

```powershell
# Check container status
docker-compose -f docker-compose.prod.yml ps

# View detailed logs
docker-compose -f docker-compose.prod.yml logs backend

# Check health status
docker inspect atlasiq-backend | findstr Health
```

### Port Already in Use

```powershell
# Check what's using port 80
netstat -ano | findstr :80

# Check what's using port 8000
netstat -ano | findstr :8000

# Stop the process or change ports in docker-compose.prod.yml
```

### Reset Everything

```powershell
# Stop and remove containers, volumes, and images
docker-compose -f docker-compose.prod.yml down -v --rmi all

# Rebuild from scratch
docker-compose -f docker-compose.prod.yml up --build -d
```

### Access Container Shell

```powershell
# Backend container
docker exec -it atlasiq-backend sh

# Frontend container
docker exec -it atlasiq-frontend sh
```

## 🔒 Security Considerations

### Production Deployment

1. **Change JWT Secret**: Use a strong random key
2. **Change Admin Password**: Immediately after first login
3. **Use HTTPS**: Deploy behind a reverse proxy (nginx/traefik)
4. **Limit Ports**: Don't expose backend port publicly
5. **Update Regularly**: Keep Docker images updated

### HTTPS Setup with Let's Encrypt

Add Traefik or nginx as reverse proxy:

```yaml
# Add to docker-compose.prod.yml
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=your@email.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik-certs:/letsencrypt
    networks:
      - atlasiq-network
```

## 📊 Monitoring

### Health Checks

Both services have built-in health checks:

```powershell
# Check backend health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost/
```

### Resource Usage

```powershell
# View resource usage
docker stats

# View specific container
docker stats atlasiq-backend atlasiq-frontend
```

## 🚢 Production Deployment

### Deploy to Cloud (AWS, Azure, GCP)

1. **Build images locally**:
   ```powershell
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Tag images**:
   ```powershell
   docker tag atlasiq-web-backend:latest your-registry/atlasiq-backend:latest
   docker tag atlasiq-web-frontend:latest your-registry/atlasiq-frontend:latest
   ```

3. **Push to registry**:
   ```powershell
   docker push your-registry/atlasiq-backend:latest
   docker push your-registry/atlasiq-frontend:latest
   ```

4. **Deploy to cloud service** (AWS ECS, Azure Container Instances, GCP Cloud Run)

## 🎯 Performance Optimization

### Frontend Optimization
- Nginx gzip compression enabled
- Static asset caching (1 year)
- Production React build (minified)

### Backend Optimization
- Python slim image (smaller size)
- SQLite for simple deployments
- Health checks for reliability

## 📝 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker images
        run: docker-compose -f docker-compose.prod.yml build
      
      - name: Run tests
        run: docker-compose -f docker-compose.prod.yml run backend pytest
      
      - name: Deploy to production
        run: |
          # Your deployment commands here
```

## 🆘 Support

For issues or questions:
1. Check logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify configuration: Check `.env` file
3. Test health: `curl http://localhost:8000/health`
4. Reset if needed: `docker-compose -f docker-compose.prod.yml down -v`

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [React Production Build](https://react.dev/learn/start-a-new-react-project#production-grade-react-frameworks)
