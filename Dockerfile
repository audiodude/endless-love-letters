FROM python:3.12
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080 --log-file=- --timeout=120"
CMD ["uv", "run", "--no-sync", "gunicorn", "app:app"]
