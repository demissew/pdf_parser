# PDF Parser Service

Production-ready PDF parsing service with Docker containerization, API key authentication, and structured logging.

## Quick Start (Docker)

The fastest way to get started is with Docker:

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Configure API keys (optional but recommended)
# Edit .env and set: PDF_PARSER_API_KEYS=your-secret-key-1,your-secret-key-2

# 3. Start the service
docker-compose up -d

# 4. Check health
curl http://localhost:29999/health
```

The service will be available at `http://localhost:29999`.

## API Endpoints

### Health Check
```bash
GET /health
```

No authentication required. Returns service health status.

```bash
curl http://localhost:29999/health
```

### Parse PDF from URL
```bash
POST /parse/pdf
```

**Authentication required** (when API keys are configured).

**Headers:**
- `X-API-Key`: Your API key
- `Content-Type`: application/json

**Body:**
```json
{
  "url": "https://example.com/document.pdf"
}
```

**Example:**
```bash
curl -X POST http://localhost:29999/parse/pdf \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/document.pdf"}'
```

### Parse PDF from File Upload
```bash
POST /parse/file
```

**Authentication required** (when API keys are configured).

**Headers:**
- `X-API-Key`: Your API key
- `Content-Type`: multipart/form-data

**Example:**
```bash
curl -X POST http://localhost:29999/parse/file \
  -H "X-API-Key: your-secret-key" \
  -F "file=@document.pdf"
```

## Authentication

API key authentication is enabled when the `PDF_PARSER_API_KEYS` environment variable is set.

### Configuration

```bash
# Single API key
PDF_PARSER_API_KEYS=your-secret-key

# Multiple API keys (comma-separated)
PDF_PARSER_API_KEYS=key1,key2,key3
```

### Usage

Include the API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secret-key" http://localhost:29999/parse/pdf
```

### Disabling Authentication

To disable authentication (not recommended for production), leave `PDF_PARSER_API_KEYS` empty or unset.

## Development Setup

### With Docker (Recommended)

Development mode includes live code reload and text-based logging:

```bash
# Start in development mode
docker-compose up

# View logs
docker-compose logs -f
```

Code changes in the `app/` directory will automatically reload the service.

### Without Docker

For local development without Docker:

```bash
# 1. Install dependencies
uv sync --all-extras

# 2. Run the service
uvicorn app.main:app --reload --port 29999

# 3. Access interactive docs (when auth is disabled)
# http://localhost:29999/docs
```

## Configuration

All configuration is managed through environment variables with the `PDF_PARSER_` prefix. See `.env.example` for all available options.

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `PDF_PARSER_API_KEYS` | _(empty)_ | Comma-separated API keys for authentication |
| `PDF_PARSER_LOG_FORMAT` | `json` | Log format: `json` (production) or `text` (development) |
| `PDF_PARSER_LOG_LEVEL` | `INFO` | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `PDF_PARSER_WORKERS` | `2` | Number of worker processes |
| `PDF_PARSER_WORKER_TIMEOUT` | `600` | Worker timeout in seconds |
| `PDF_PARSER_DOCLING_DEVICE` | `auto` | Processing device: `auto`, `cpu`, or `cuda` |
| `PDF_PARSER_MAX_UPLOAD_MB` | `25` | Maximum upload size in megabytes |

### GPU Support

The service automatically detects and uses GPU when available (`PDF_PARSER_DOCLING_DEVICE=auto`). To force CPU-only:

```bash
PDF_PARSER_DOCLING_DEVICE=cpu
```

## Monitoring & Logging

### Structured Logging

The service uses structured JSON logging in production for easy parsing and analysis:

```json
{
  "timestamp": "2026-01-30T12:34:56.789Z",
  "level": "INFO",
  "name": "app.api.middleware",
  "message": "Request completed",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "method": "POST",
  "path": "/parse/pdf",
  "status_code": 200,
  "duration_ms": 1234.56
}
```

### Request Tracing

Every request receives a unique `X-Request-ID` header for tracing:

```bash
curl -I http://localhost:29999/health
# HTTP/1.1 200 OK
# X-Request-ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### Viewing Logs

```bash
# View logs (Docker)
docker-compose logs -f

# View logs with timestamps
docker-compose logs -f --timestamps

# View logs for specific time range
docker-compose logs --since 10m
```

### Health Checks

Docker includes automatic health checks:

```bash
# Check container health
docker ps

# View health check logs
docker inspect pdf_parser --format='{{json .State.Health}}' | jq
```

## Testing

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_auth.py

# Run with coverage
uv run pytest --cov=app

# Run with verbose output
uv run pytest -v
```

## Deployment

### Production Server Setup

Before deploying, prepare your production server:

#### 1. Install Docker

```bash
# Update system
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install docker-compose
sudo apt-get install docker-compose-plugin

# Add user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. Create Deployment Directory

```bash
# Create directory for the application
sudo mkdir -p /opt/pdf_parser
sudo chown $USER:$USER /opt/pdf_parser
cd /opt/pdf_parser
```

#### 3. Setup Environment File

```bash
# Create production .env file
cat > .env << 'EOF'
# Application Settings
PDF_PARSER_APP_NAME=pdf_parser
PDF_PARSER_TEMP_DIR=/tmp/pdf_parser
PDF_PARSER_MAX_UPLOAD_MB=25

# Logging
PDF_PARSER_LOG_LEVEL=INFO
PDF_PARSER_LOG_FORMAT=json

# Authentication - IMPORTANT: Set strong API keys for production!
PDF_PARSER_API_KEYS=your-super-secret-key-1,your-super-secret-key-2

# Server Configuration
PDF_PARSER_WORKERS=4
PDF_PARSER_WORKER_TIMEOUT=600

# Docling Configuration
PDF_PARSER_DOCLING_NUM_THREADS=2
PDF_PARSER_DOCLING_DEVICE=auto
PDF_PARSER_DOCLING_TIMEOUT_S=500.0
PDF_PARSER_DOCLING_MAX_NUM_PAGES=300
PDF_PARSER_DOCLING_MAX_FILE_SIZE_MB=25
EOF

# Secure the .env file
chmod 600 .env
```

**IMPORTANT:** Generate strong, random API keys for production:
```bash
# Generate secure API keys
openssl rand -hex 32  # Use this output as your API key
```

#### 4. Clone Repository

```bash
# Clone the repository into the deployment directory
cd /opt/pdf_parser
git clone https://github.com/your-username/pdf_parser.git .

# Verify docker-compose.yml exists (it's in the repo)
ls -la docker-compose.yml
```

### GitHub Actions Deployment (Recommended)

#### Prerequisites

1. **Server Setup:** Complete the Production Server Setup steps above
2. **Git Repository:** Your production server must have git access to the repository
3. **GitHub Secrets:** Configure the following secrets in your repository (Settings → Secrets and variables → Actions):

**SSH Access:**
- `SSH_HOST`: Server hostname or IP address
- `SSH_USER`: SSH username (e.g., `ubuntu`, `root`)
- `SSH_PORT`: SSH port (typically `22`)
- `SSH_PASSWORD`: SSH password

**Configuration:**
- `ENV_FILE`: Complete production environment variables (paste entire contents of production `.env` file)
- `REMOTE_PATH`: Deployment directory on server (e.g., `/opt/pdf_parser`)
- `HEALTH_URL`: Health check endpoint (default: `http://localhost:29999/health`)

#### Deployment Steps

1. **Initial Setup on Server:**
   ```bash
   # SSH into server
   ssh user@your-server

   # Create deployment directory
   sudo mkdir -p /opt/pdf_parser
   sudo chown $USER:$USER /opt/pdf_parser
   cd /opt/pdf_parser

   # Clone repository
   git clone https://github.com/your-username/pdf_parser.git .

   # Create .env file (see Production Server Setup section)
   nano .env
   ```

2. **Trigger Deployment:**
   - Go to GitHub → Actions → "Deploy (Docker)"
   - Click "Run workflow"
   - Select environment (`ne`)
   - Click "Run workflow"

3. **Monitor Progress:**
   - Watch the workflow execution in real-time
   - The workflow will SSH into your server and execute deployment

4. **Verify Deployment:**
   ```bash
   # On your production server
   docker ps
   curl http://localhost:29999/health
   curl -H "X-API-Key: your-api-key" -X POST http://localhost:29999/parse/pdf \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/test.pdf"}'
   ```

The workflow automatically:
- Pulls latest code from git
- Builds Docker image locally on server
- Stops old container
- Starts new container
- Runs health checks (20 retries × 3 seconds)
- Rolls back to previous container on failure
- Cleans up old images (keeps last 5)

### Manual Deployment

For manual deployment to a production server:

#### Initial Setup

```bash
# 1. SSH into your server
ssh user@your-server

# 2. Navigate to deployment directory
cd /opt/pdf_parser

# 3. Clone repository
git clone https://github.com/your-username/pdf_parser.git .

# 4. Ensure .env file exists (see Production Server Setup above)
cat .env  # Verify configuration

# 5. Build and start the service
docker-compose build
docker-compose up -d

# 6. Check status
docker ps
docker-compose logs -f
```

#### Updating Deployment

```bash
# 1. Navigate to deployment directory
cd /opt/pdf_parser

# 2. Pull latest code
git pull

# 3. Rebuild image
docker-compose build

# 4. Stop old container
docker-compose down

# 5. Start new container
docker-compose up -d

# 6. Verify health
curl http://localhost:29999/health

# 7. Check logs
docker-compose logs -f
```

### Rollback Procedures

#### Automatic Rollback

GitHub Actions includes automatic rollback on health check failure. The previous container is automatically restarted.

#### Manual Rollback

```bash
# 1. Navigate to deployment directory
cd /opt/pdf_parser

# 2. View git history
git log --oneline -10

# 3. Checkout previous version
git checkout <previous-commit-sha>

# 4. Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# 5. Verify
curl http://localhost:29999/health

# 6. To return to latest, checkout main branch
git checkout main
```

### Production Checklist

Before going to production, verify:

- [ ] Strong API keys configured in `.env`
- [ ] `PDF_PARSER_LOG_FORMAT=json` for structured logging
- [ ] Appropriate resource limits set in `docker-compose.yml`
- [ ] Health check endpoint returns 200 OK
- [ ] Authentication working (parse endpoints require API key)
- [ ] Logs are being captured and monitored
- [ ] Firewall configured (only port 29999 exposed if needed)
- [ ] SSL/TLS termination configured (if exposing to internet)
- [ ] Backup strategy in place (for logs and data if needed)
- [ ] Monitoring and alerting configured
- [ ] Rollback procedure tested

### Security Recommendations

1. **API Keys:** Use strong, randomly generated keys
2. **Network:** Use reverse proxy (nginx/traefik) with SSL
3. **Firewall:** Restrict access to port 29999
4. **Updates:** Regularly update base image and dependencies
5. **Secrets:** Never commit `.env` or API keys to git
6. **Logs:** Regularly review logs for suspicious activity
7. **Resources:** Set appropriate memory/CPU limits

## Troubleshooting

### Container won't start

Check logs for errors:

```bash
docker-compose logs
```

Common issues:
- Missing environment variables (check `.env`)
- Port 29999 already in use
- Insufficient memory (requires ~1GB)

### Authentication failing

Verify API keys are configured correctly:

```bash
# Check environment
docker-compose exec pdf_parser env | grep API_KEYS

# Test with correct key
curl -H "X-API-Key: your-key" http://localhost:29999/health
```

### Out of memory

Increase Docker memory limits in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 8G  # Increase as needed
```

### Slow processing

Increase workers or timeout:

```bash
PDF_PARSER_WORKERS=4
PDF_PARSER_WORKER_TIMEOUT=1200
```

### GPU not detected

Verify GPU support:

```bash
# Check GPU availability
docker-compose exec pdf_parser nvidia-smi

# Force GPU usage
PDF_PARSER_DOCLING_DEVICE=cuda
```

If GPU is not available, the service will automatically fall back to CPU.

## Architecture

### Components

- **FastAPI**: Web framework and API routing
- **Gunicorn**: Production WSGI server with process management
- **Uvicorn**: ASGI worker for async request handling
- **Docling**: PDF parsing and document processing
- **Docker**: Containerization and deployment

### Security Features

- Non-root container execution
- API key authentication
- No Swagger UI in production (when auth enabled)
- Request/response logging for audit trails
- Resource limits to prevent DoS

### Performance

- Multi-worker process model
- Async request handling
- GPU acceleration (when available)
- Configurable timeouts and limits

## License

See LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check logs: `docker-compose logs -f`
- Review configuration: `.env.example`
