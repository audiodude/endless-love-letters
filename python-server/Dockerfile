FROM python:3.12
WORKDIR /app

RUN pip3 install --no-cache-dir pipenv
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080 --log-file=-"
CMD ["gunicorn", "app:app"]
