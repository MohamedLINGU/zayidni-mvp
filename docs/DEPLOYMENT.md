Staging deployment checklist (minimal)

1. Provision infrastructure
   - Create a DigitalOcean project or equivalent
   - Provision Postgres (managed), Redis (managed), and object storage (Spaces or S3-compatible)
   - Configure domain and TLS (Let's Encrypt)

2. Environment variables (example)
   - DJANGO_SECRET_KEY
   - DATABASE_URL / POSTGRES_* (host, user, password)
   - REDIS_URL
   - CELERY_BROKER_URL (usually same as REDIS_URL)
   - EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD
   - PAYMENT_* sandbox keys (when integrating)

3. App deployment
   - Build and collect static files
   - Run migrations: python manage.py migrate
   - Start ASGI server (daphne/uvicorn/gunicorn + uvicorn workers)
   - Start Celery worker and beat

4. Observability
   - Add basic logging (stdout) and set up a log drain
   - Configure health checks for web and celery
   - Set up backups for Postgres and object storage

5. Sanity checks
   - Create test users, listings, run a demo auction, simulate payment via sandbox
   - Verify WebSocket connectivity (Channels + Redis)

Notes:
- This checklist is intentionally minimal for a staging environment. Production requires hardening, WAF, rate-limiting, monitoring, and legal checks (no real-estate category until legal reviewed).
