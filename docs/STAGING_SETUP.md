Staging provisioning guide (recommended minimal steps)

1. Provision servers
   - Create a small droplet (or equivalent) for the app (2 vCPU, 4GB RAM recommended)
   - Alternatively use a managed container service and attach managed Postgres/Redis

2. DNS & TLS
   - Point staging hostname (e.g., staging.zayidni.example.com) to the server IP
   - Install certbot and obtain a TLS certificate or use a load balancer with TLS

3. Install prerequisites on the server
   - docker, docker-compose (v2+), rsync, git, python (optional for helpers)
   - Create a system user (e.g., "deploy") with an SSH key for automated deploys

4. Create .env.staging on the server
   - Copy .env.staging.example and set real values (SECRET_KEY, DB credentials, REDIS_URL)

5. Run initial deploy
   - From CI runner or local machine:
       export STAGING_SSH=deploy@staging.example.com
       export STAGING_PATH=/home/deploy/apps/zayidni
       ./scripts/deploy_staging.sh

6. Verify
   - Visit the staging URL; ensure web responds and websockets connect
   - Check Celery worker and beat logs: docker compose -f docker-compose.staging.yml logs -f celery

7. Notes & Security
   - Use strong passwords for Postgres and restrict access via UFW or cloud firewall
   - Configure backups for Postgres and object storage
   - For production, consider managed DB/Redis, WAF, and secrets manager
