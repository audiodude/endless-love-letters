import os

import dotenv


dotenv.load_dotenv()


def secret(name):
  return os.environ[name]


def get_secret(name):
  val = os.environ.get(name)
  if name == 'MYSQL_PORT':
    return val and int(val)
  return val