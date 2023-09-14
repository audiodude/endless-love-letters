import mailbox
import random
import quopri

import bs4


def get_html_text(html):
  root = bs4.BeautifulSoup(html, 'lxml')

  top_div = root.contents[0].find('div')
  if not top_div:
    return None

  divs = top_div.find_all('div')
  if not divs:
    return None

  return '\n'.join(['Dear Abby,'] + [div.get_text() for div in divs])


class GmailMboxMessage():

  def __init__(self, email_data):
    if not isinstance(email_data, mailbox.mboxMessage):
      raise TypeError('Variable must be type mailbox.mboxMessage')
    self.email_data = email_data
    self.payload = self.read_email_payload()

  def read_email_payload(self):
    email_payload = self.email_data.get_payload()
    if self.email_data.is_multipart():
      email_messages = list(self._get_email_messages(email_payload))
    else:
      email_messages = [email_payload]
    return [self._read_email_text(msg) for msg in email_messages]

  def _get_email_messages(self, email_payload):
    for msg in email_payload:
      if isinstance(msg, (list, tuple)):
        for submsg in self._get_email_messages(msg):
          yield submsg
      elif msg.is_multipart():
        for submsg in self._get_email_messages(msg.get_payload()):
          yield submsg
      else:
        yield msg

  def _read_email_text(self, msg):
    content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
    encoding = 'NA' if isinstance(msg, str) else msg.get(
        'Content-Transfer-Encoding', 'NA')
    if 'text/plain' in content_type and 'base64' not in encoding:
      msg_text = msg.get_payload()
    elif 'text/html' in content_type and 'base64' not in encoding:
      self.raw_html = msg.get_payload(decode=True)
      msg_text = get_html_text(self.raw_html)
    elif content_type == 'NA':
      msg_text = get_html_text(msg)
    else:
      msg_text = None
    return (content_type, encoding, msg_text)


mbox_obj = mailbox.mbox('daily_love_letters.mbox')
parsed_emails = [GmailMboxMessage(email_obj) for email_obj in mbox_obj]
email_htmls = [
    payload[2]
    for email in parsed_emails
    for payload in email.payload
    if payload[0] == 'text/html' and payload[2] is not None
]

random_email = random.choice(email_htmls)
print(random_email)
