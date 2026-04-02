import json

import parse_emails


def create_search_documents():
  for email in parse_emails.get_emails():
    if email[1][0] is None:
      continue

    yield json.dumps({'letter': email[0], 'id': email[1][0]})
    if email[1][1] is not None:
      yield json.dumps({'letter': email[0], 'id': email[1][1]})


def create_search_output():
  with open('search_documents.jsonl', 'w') as f:
    f.write('\n'.join(create_search_documents()))
