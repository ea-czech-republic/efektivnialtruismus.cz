FROM python:3.6-slim as production

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir --upgrade pip pipenv && \
    pipenv install --system --deploy


COPY website ./website
RUN python website/manage.py collectstatic --no-input

COPY bin/run.sh bin/run.sh
