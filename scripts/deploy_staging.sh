#!/usr/bin/env bash
set -euo pipefail

# deploy_staging.sh
# Usage (locally):
#   export STAGING_SSH=user@staging-host
#   export STAGING_PATH=/home/user/apps/zayidni
#   ./scripts/deploy_staging.sh

if [ -z "${STAGING_SSH:-}" ] || [ -z "${STAGING_PATH:-}" ]; then
  echo "Please set STAGING_SSH and STAGING_PATH environment variables."
  exit 1
fi

LOCAL_TMP=./deploy_tmp
RSYNC_OPTS='-az --delete --exclude .git --exclude node_modules --exclude .venv'

echo "Packaging code..."
rm -rf "$LOCAL_TMP" && mkdir -p "$LOCAL_TMP"
rsync $RSYNC_OPTS . "$LOCAL_TMP/"

echo "Syncing to $STAGING_SSH:$STAGING_PATH"
ssh "$STAGING_SSH" "mkdir -p $STAGING_PATH"
rsync $RSYNC_OPTS "$LOCAL_TMP/" "$STAGING_SSH:$STAGING_PATH/"

echo "Installing on remote and starting services (docker-compose)..."
ssh "$STAGING_SSH" bash -lc "cd $STAGING_PATH && docker compose -f docker-compose.staging.yml pull && docker compose -f docker-compose.staging.yml up -d --build && \
  docker compose -f docker-compose.staging.yml exec -T web python manage.py migrate --noinput && \
  docker compose -f docker-compose.staging.yml exec -T web python manage.py collectstatic --noinput"

echo "Deployment complete."

# cleanup
rm -rf "$LOCAL_TMP"
