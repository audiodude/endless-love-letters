import json
import os

from parse_emails import get_emails

DATA_DIR = os.environ.get('DATA_DIR', '.')

SEARCH_DOCS_PATH = os.path.join(DATA_DIR, 'search_documents.jsonl')
MBOX_PATH = os.path.join(DATA_DIR, 'daily_love_letters.mbox')

# Load existing search documents
DATABASE = {}
if os.path.exists(SEARCH_DOCS_PATH):
    with open(SEARCH_DOCS_PATH) as f:
        for line in f:
            if line.strip():
                doc = json.loads(line)
                DATABASE[doc['id']] = doc['letter']

# Parse mbox and append any new letters
if os.path.exists(MBOX_PATH):
    new_docs = []
    for text, ids in get_emails(MBOX_PATH):
        primary_id, secondary_id = ids
        if primary_id is None:
            continue
        if primary_id not in DATABASE:
            DATABASE[primary_id] = text
            new_docs.append(json.dumps({'letter': text, 'id': primary_id}))
        if secondary_id is not None and secondary_id not in DATABASE:
            DATABASE[secondary_id] = text
            new_docs.append(json.dumps({'letter': text, 'id': secondary_id}))

    if new_docs:
        with open(SEARCH_DOCS_PATH, 'a') as f:
            f.write('\n' + '\n'.join(new_docs))
        print(f'Appended {len(new_docs)} new letters to search_documents.jsonl')

ALL_LETTERS = list(DATABASE.values())
