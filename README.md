# Switchback Backend
A rococo-based backend for Switchback TodoMVC application

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)

## Setup

1. **Create `.env.secrets` file** (copy from `.env.secrets.example`):
   ```bash
   cp .env.secrets.example .env.secrets
   ```

2. **Edit `.env.secrets`** and replace all placeholder values with actual secrets:
   - Generate secure random strings for `SECRET_KEY`, `SECURITY_PASSWORD_SALT`, `AUTH_JWT_SECRET`
   - Set `POSTGRES_PASSWORD` and `RABBITMQ_PASSWORD`
   - Add your Mailjet API credentials (`MAILJET_API_KEY`, `MAILJET_API_SECRET`)
   - The first line must be: `APP_ENV=local` (or `test`/`production`)

3. **Ensure `local.env` exists** (it should already be in the repo)

## Running the Application

### Start the backend:
```bash
./run.sh
```

### Rebuild and start (if you've made changes to Dockerfiles):
```bash
./run.sh --rebuild true
```

### Check if services are running:
```bash
docker ps
```

### View logs:
```bash
docker logs switchback_api
```

### Stop the backend:
```bash
docker compose down
```