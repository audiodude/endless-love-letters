# Endless Love Letters

This is the source code for the site at https://endless-love-letters.com

Since 2019, I have written my wife Abby a love letter every day, for a total of
1458 captured at the time of the Google Takeout export.

These scripts take an `.mbox` file with a bunch of love letter emails, parse
them out, feed them to the OpenAI GPT 3.5 finetuning API to finetune a model,
then generate new love letters.

The web interface includes both v1 (static love letter list generated with some
pre-GPT charNN-like solution whose name has been lost) and v2 (love letters
generated on the fly with ChatGPT).

## Populating the .env file with secrets

The Python code uses [dotenv](https://github.com/theskumar/python-dotenv) to
manage secrets. Look at .env.example for which values are required. Neither the
site nor the command line tools will function without the secrets being set.

## Generating a love letter offline

Offline meaning without the web app, this still contacts the OpenAI API.

Just run:

```bash
python generate.py
```

Note that the prompts and model id are hardcoded into the script.

# Favorites

## v1

In v1, all love letters have a specific ID (they are pre-generated and stored in
`static/data/letters.json`). For saving favorites, a list of IDs is stored in a
cookie in JSON format.

## v2, MySQL database

The MySQL database is extremely tiny, and is used to store the user's v2
favorite generated love letters. The entire love letter text is stored in a
single column. Users are anonymous, and are assigned an id (which is stored in
their browser cookies) the first time they attempt to favorite a love letter.

## Generating the database

Connect to the MySQL database server, then run:

```sql
CREATE DATABASE endless_love_letters;
```

Then load the schema:

```bash
mysql -u <user> -p endless_love_letters < schema.sql
```

# Searching

The complete love letter corpus is stored in `search_documents.jsonl`. This is a
"JSON lines" formatted data file, with one object containing one love letter on
each line. The file is "baked in" to the Python application server, and loaded
directly into a Python dictionary at start up. It is also baked into the
Javascript (Deno) application server, where it is used for full text search

The search service is protected by a single password (for privacy reasons) that
is set using `WEB_PASSWORD` environment variable to the Python server.

## Generating `search_documents.jsonl`

This file is mapped directly from the same process that processes the `.mbox`
file for generating finetuning data. To generate it, put the
`daily_love_letters.mbox` (retrieved from Google Takeout) in the python-server
directory. Then start a Python shell (with pipenv) and run the following
commands:

```bash
$ pipenv run python
Python 3.12.0 (main, Oct  3 2023, 17:47:52) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import documents
>>> documents.create_search_output()
>>>
```

# Development

## Running the search server locally

The search server URL is specified in the Python environment as
`SEARCH_SERVER_URL`. The Python Flask server connects to it on search requests.
To run the sever, cd into the `deno-server` directory and run:

```bash
deno run --allow-read --allow-env --allow-net main.ts
```

## Running the Python web app locally

From the python-server directory:

```bash
SEARCH_SERVER_URL=localhost:3000 WEB_PASSWORD=fakepassword pipenv run flask --debug -A app run
```

# Deploying to fly,io

1. Install the Fly.io command line tool, `flyctl`

```bash
fly deploy
```
