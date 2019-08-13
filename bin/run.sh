#!/usr/bin/env sh
set -e

# Build the command line (note that sh shell does not have proper arrays)
if [ "${DEBUG}" = "True" ]; then
    RELOAD="--reload "
else
    RELOAD=""
fi

python website/manage.py migrate
python website/manage.py collectstatic --noinput --clear

cat <<EOF | python website/manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

print('\n\n')

if User.objects.filter(username='admin').exists():
    print('admin user exists, not creating...')
else:
    User.objects.create_superuser('admin', 'admin@example.com', 'pass')
    print('Created admin user with password pass')

print('\n\n')

EOF

exec gunicorn eacr.wsgi \
    --bind 0.0.0.0:8000 \
    --name eacr-app-server \
    --chdir "$(pwd)"/website \
    ${RELOAD}
