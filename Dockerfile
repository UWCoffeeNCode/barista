FROM python:3.8-alpine AS builder

# Install build dependencies.
RUN pip install pipenv

# Copy source code.
WORKDIR /src
COPY Pipfile Pipfile.lock ./

# Generate requirements.txt
RUN pipenv lock -r > requirements.txt


FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

# Copy requirements.txt
WORKDIR /app
COPY --from=builder /src/requirements.txt ./

# Install dependencies.
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# Copy app code.
COPY barista/ ./barista/
COPY manage.py ./

# Configure Gunicorn.
ENV MODULE_NAME=barista.asgi VARIABLE_NAME=application

# Collect static files.
RUN BARISTA_SECRET=dummy python manage.py collectstatic

# Open ports.
EXPOSE 80
