FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    python3-dev \
    gcc \
    musl-dev \
    libffi-dev \
    libpq \
    postgresql-dev \
    build-base \
    linux-headers

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["/app/docker/backend/development/server-entrypoint.sh"]

