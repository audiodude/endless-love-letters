import json
import os
import sys

import requests

from get_secrets import secret

OPENAPI_TOKEN = secret('OPENAPI_TOKEN')


def generate():
  data = {
      'model': 'ft:gpt-3.5-turbo-0613:personal::7ybccOXf',
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
      }],
      'stop': 'Love Forever,\n-Travis',
  }

  r = requests.post('https://api.openai.com/v1/chat/completions',
                    headers={'Authorization': 'Bearer %s' % OPENAPI_TOKEN},
                    json=data)
  if not r.ok:
    print(r.text)
    return

  output = r.json()
  try:
    return output['choices'][0]['message']['content'] + 'Love Forever,\n-Travis'
  except KeyError:
    print(output)


if __name__ == '__main__':
  letter = generate()
  print(letter)
