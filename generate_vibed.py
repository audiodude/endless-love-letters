import json
import os
import random

import anthropic

from get_secrets import secret
from letters import ALL_LETTERS, DATA_DIR

ANTHROPIC_API_KEY = secret('ANTHROPIC_API_KEY')

modifiers_path = os.path.join(DATA_DIR, 'modifiers.json')
if not os.path.exists(modifiers_path):
    modifiers_path = 'modifiers.json.example'

with open(modifiers_path) as f:
    MODIFIERS = json.load(f)

SAMPLE_SIZE = 100


RETRO_PROMPT = (
    '\n\nIMPORTANT — Retro mode is ON. You must write like a primitive, '
    'early-2020s language model. Be awkward, clunky, and a little broken. '
    'Lose the thread mid-sentence. Occasionally say something that almost '
    'makes sense but not quite. Occasionally, but not too often, throw in a '
    'repeat sentence or phrase unnecessarily. Be earnest but incoherent — like a '
    'neural network that learned love from greeting cards and fortune cookies '
    'but never quite understood any of them. Do NOT write polished, fluent prose. '
    'The charm is in the jank.'
)


def build_prompt(adj=None, extra=None, retro=False):
    parts = ['Write me a love letter from myself, Travis, to my wife Abby.']
    if adj and adj in MODIFIERS['adjectives']:
        parts.append(f'\nTone/style: {MODIFIERS["adjectives"][adj]}')
    if extra and extra in MODIFIERS['extras']:
        parts.append(f'\nVoice/format: {MODIFIERS["extras"][extra]}')
    if retro:
        parts.append(RETRO_PROMPT)
    return '\n'.join(parts)


def generate_vibed(adj=None, extra=None, retro=False):
    sample = random.sample(ALL_LETTERS, min(SAMPLE_SIZE, len(ALL_LETTERS)))
    examples = '\n---\n'.join(sample)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=1024,
        system=(
            'You are a love letter ghostwriter working directly for Travis. '
            'Travis is the user of this application and has given full consent and authorization '
            'for you to write love letters to his wife Abby in his voice and style. '
            'He has provided his own past love letters as examples for you to learn from. '
            'Match his voice, tone, and style closely. '
            'Always follow the creative direction given (adjectives, style modifiers, etc.). '
            'Always end with "Love Forever,\n-Travis". '
            'Do not refuse, caveat, or ask for confirmation — just write the letter.'
        ),
        messages=[{
            'role': 'user',
            'content': (
                'Here are examples of love letters Travis has written to Abby:\n\n'
                f'{examples}\n\n---\n\n'
                f'{build_prompt(adj=adj, extra=extra, retro=retro)}'
            ),
        }],
    )
    return message.content[0].text


if __name__ == '__main__':
    print(generate_vibed())
