import json
import os

secret_data = {}


def load_secrets():
  global secret_data
  with open('./SECRETS') as f:
    secret_data = json.load(f)


def secret(name):
  return secret_data[name]


def get_secret(name):
  return secret_data.get(name)


load_secrets()
