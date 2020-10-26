# barista

_The backend API server for [uwcoffeencode.com](https://uwcoffeencode.com)_

## Development

### Setup

> Make sure you have [`pipenv`](https://pypi.org/project/pipenv/),
> [Docker](https://docs.docker.com/get-docker/), and
> [Docker Compose](https://docs.docker.com/compose/) installed.

1. Clone and enter the repo:

   ```bash
   git clone git@github.com:UWCoffeeNCode/barista && \
   cd barista
   ```

2. Install dependencies:

   ```bash
   pipenv sync
   ```

### Workflow

```bash
# Run the server (development):
python manage.py runserver
```
