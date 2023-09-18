# Endless Love Letters

This is the source code for the site at https://endless-love-letters.com

Since 2019, I have written my wife Abby a love letter every day, for a total of 1458 captured
at the time of the Google Takeout export.

These scripts take an `.mbox` file with a bunch of love letter emails, parse them out, feed them to
the OpenAI GPT 3.5 finetuning API to finetune a model, then generate new love letters.

The web interface includes both v1 (static love letter list generated with some pre-GPT charNN-like
solution whose name has been lost) and v2 (love letters generated on the fly with ChatGPT).

## Populating the SECRETS file

Look at `SECRETS.example` for the tokens which should go into `SECRETS`, which is a JSON file.
Neither the site nor the command line tools will function without the `SECRETS` being set.

## Generating a love letter offline

Offline meaning without the web app, this still contacts the OpenAI API.

Just run:

```bash
python generate.py
```

Note that the prompts and model id are hardcoded into the script.

## Generating the database

In MySQL, run:

```sql
CREATE DATABASE endless_love_leeters;
```

Then load the schema:

```bash
mysql -u <user> -p endless_love_letters < schema.sql
```

## Running the web app locally

```bash
FLASK_DEBUG=1 FLASK_APP=app flask run
```

## Deploying to fly,io

1. Install the Fly.io command line tool, `flyctl`
2. Update the SECRETS file to contain the production values. Then:

```bash
fly deploy
```
