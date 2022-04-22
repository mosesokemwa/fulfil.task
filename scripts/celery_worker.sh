#!/bin/bash

set -o errexit
set -o nounset

# celery -A app.celery worker --loglevel=info
# -A app.celery_task worker -l INFO