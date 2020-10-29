# barista

_The backend API server for [uwcoffeencode.com](https://uwcoffeencode.com)_

[![Build Status][drone-img]][drone]

## Usage

### Public API

The public API is served at
[api.uwcoffeencode.com](https://api.uwcoffeencode.com).
This is the address that internal and external applications will use to
fetch Coffee 'N Code-related data.

Some information can only be accessed by **authenticated** clients.
To authenticate, a user must perform a `login` mutation:

```graphql
mutation Login($username: String!, $password: String!) {
  login(input: { username: $username, password: $password }) {
    user {
      id
    }
  }
}
```

Only first-party browser clients may authenticate with the API and
read/update private data; third-party browser clients may only make use of
public data.

### Administration

The admin console is served at
[barista.uwcoffeencode.com](https://barista.uwcoffeencode.com). Staff users
(i.e. us) can login and securely manage backend data without direct database
access.

<br />

## Development

### Setup

> Make sure you have [`pyenv`](https://github.com/pyenv/pyenv),
> [`pipenv`](https://pypi.org/project/pipenv/),
> [Docker](https://docs.docker.com/get-docker/), and
> [Docker Compose](https://docs.docker.com/compose/) installed.

1. Clone and enter the repo:

   ```bash
   git clone git@github.com:UWCoffeeNCode/barista && \
   cd barista
   ```

2. Install dependencies:

   ```bash
   # Install dependencies from `Pipfile.lock`:
   pipenv sync
   ```

3. Configure `.env`:

   ```bash
    # Copy env values from example template:
    cp .env.example > .env

    # Edit to use real values:
    vi .env
   ```

### Workflow

To get started, go ahead and do the following:

```bash
# Launch external systems (database, etc.):
docker-compose up -d

# Run database migrations:
python manage.py migrate

# Run the server (development):
python manage.py runserver
```

Some useful commands include:

```bash
# Run the shell (administration):
python manage.py shell
```

[drone]: https://ci.stevenxie.me/UWCoffeeNCode/barista
[drone-img]: https://ci.stevenxie.me/api/badges/UWCoffeeNCode/barista/status.svg
