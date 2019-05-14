FROM python:3.6-slim as production

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir --upgrade pip pipenv
COPY Pipfile Pipfile.lock ./
COPY website ./

RUN pipenv install --system --deploy