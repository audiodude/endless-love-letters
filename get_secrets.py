import os

import dotenv

dotenv.load_dotenv()


def secret(name):
  val = os.environ.get(name)
  print(f'{name}={val}')
  if name == 'MYSQL_PORT':
    return val and int(val)
  return val
