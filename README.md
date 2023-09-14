# Endless Love Letters

These scripts take an `.mbox` file with a bunch of love letter emails, parse them out, feed them to
the OpenAI GPT 3.5 finetuning API to finetune a model, then generate new love letters.

In the future, there will be a web interface for this.

## Generating a love letter

Just run:

```bash
OPENAPI_TOKEN=<token> python generate.py
```

Note that the prompts and model id are hardcoded into the script.
