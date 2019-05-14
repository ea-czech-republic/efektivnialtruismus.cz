#!/user/bin/env sh
set -e

# Build the command line (note that sh shell does not have proper arrays)
if [ "${APP_DEBUG_MODE}" = "True" ]; then
    RELOAD="--reload "
else
    RELOAD=""
fi

exec gunicorn eacr.wsgi \
    --bind 0.0.0.0:8000 \
    --name eacr-app-server \
    --workers "${GUNICORN_WORKER_COUNT}" \
    --timeout "${GUNICORN_WORKER_TIMEOUT}" \
    --max-requests "${GUNICORN_MAX_REQUESTS}" \
    --chdir "$(pwd)"/squad \
    --log-config "$(pwd)"/conf/gunicorn-logging.conf \
    --access-logformat "{'method': '%(m)s', 'url': '%(U)s', 'status': '%(s)s', 'took': %(L)s, 'remote': '%(h)s', 'size': %(b)s}" \
    ${RELOAD}