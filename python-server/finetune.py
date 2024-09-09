import json
import os
import sys

import requests

import parse_emails

OPENAPI_TOKEN = os.getenv('OPENAPI_TOKEN')


def prepare_input_messages(emails):
  return [
      json.dumps({
          'messages': [{
              'role':
                  'system',
              'content':
                  'You are an assistant that writes short, sweet love letters from Travis to Abby'
          }, {
              'role':
                  'user',
              'content':
                  'Write me a love letter from myself, Travis, that I can send to my wife Abby'
          }, {
              'role': 'assistant',
              'content': email,
          }]
      }) for email in emails
  ]


def write_finetune_file():
  with open('finetune.jsonl', 'w') as f:
    f.write('\n'.join(prepare_input_messages(parse_emails.get_email_texts())))


def upload_fine_tune_file():
  headers = {'Authorization': 'Bearer %s' % OPENAPI_TOKEN}
  files = {'file': open('finetune.jsonl', 'rb')}
  r = requests.post('https://api.openai.com/v1/files',
                    headers=headers,
                    files=files,
                    data={'purpose': 'fine-tune'})
  data = r.json()
  return data['id']


def start_finetune_job():
  fine_tune_job = {'training_file': file_id, 'model': 'gpt-3.5-turbo-0613'}
  headers = {
      'Authorization': 'Bearer %s' % OPENAPI_TOKEN,
      'Content-Type': 'application/json'
  }
  r = requests.post('https://api.openai.com/v1/fine_tuning/jobs',
                    headers=headers,
                    json=fine_tune_job)

  return r.text


if __name__ == '__main__':
  if not os.path.exists('finetune.jsonl'):
    write_finetune_file()
    file_id = upload_fine_tune_file()
  else:
    file_id = sys.argv[1]

  print(start_finetune_job())
