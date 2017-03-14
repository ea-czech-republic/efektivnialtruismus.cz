#!/usr/bin/env bash
# run this from the git repo root dir

NAME="efektivni-altruismus.cz"
DJANGODIR=website
SOCKFILE=run/gunicorn.sock
USER=$USER
GROUP=$GROUP
NUM_WORKERS=3
DJANGO_WSGI_MODULE=eacr.wsgi

echo "Starting $NAME as $EA_USER:$EA_GROUP"

# Activate the virtual environment
source .venv/bin/activate
cd $DJANGODIR
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$EA_USER --group=$EA_GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
