import json
import os
import sys

import requests

from get_secrets import secret

OPENAPI_TOKEN = secret('OPENAPI_TOKEN')


def build_content(adj=None, extra=None):
  adj = adj + ' ' if adj else ''
  extra = extra + ', ' if extra else ''
  return f'Write me a {adj}love letter from myself, Travis, {extra}that I can send to my wife Abby'


def generate(content=None, adj=None, extra=None):
  content = content or build_content(adj=adj, extra=extra)
  data = {
      'model': 'ft:gpt-3.5-turbo-0613:personal::9bj6wDbN',
      'messages': [{
          'role':
              'system',
          'content':
              'You are an assistant that writes short, sweet love letters from Travis to Abby'
      }, {
          'role': 'user',
          'content': f'{content}'
      }],
      'stop': 'Love Forever,\n-Travis',
  }

  r = requests.post('https://api.openai.com/v1/chat/completions',
                    headers={'Authorization': 'Bearer %s' % OPENAPI_TOKEN},
                    json=data)
  output = r.json()
  try:
    return output['choices'][0]['message']['content'] + 'Love Forever,\n-Travis'
  except KeyError:
    print(output)


if __name__ == '__main__':
  letter = generate()
  print(letter)
