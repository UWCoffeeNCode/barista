FROM python:3.8-alpine AS builder

# Install build dependencies.
ENV PATH="/root/.local/bin:$PATH"
RUN pip install --user pipenv

# Copy source code.
WORKDIR /src
COPY Pipfile Pipfile.lock ./

# Generate requirements.txt
RUN pipenv lock -r > requirements.txt


FROM python:3.8-alpine

# Copy requirements.txt
WORKDIR /app
COPY --from=builder /src/requirements.txt ./

# Install dependencies.
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# Copy source code.
COPY barista/ ./barista/
COPY manage.py ./

# Open ports.
EXPOSE 8000

# Define entrypoint.
ENTRYPOINT [ "python", "manage.py" ]
CMD [ "runserver" ]
