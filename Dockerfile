FROM python:3.11.5-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080 --log-file=-"
CMD ["gunicorn", "app:app"]
