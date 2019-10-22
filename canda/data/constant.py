
import base64
import os
from string import Template

_template = """Account: $account
Username: $username
Password: $password
"""

DETAILS_TEMPLATE = Template(_template)
RECORDS = []
SALT = base64.b64decode(os.environ['CANDA_SALT'])
LOGIN_TOKEN = os.environ['CANDA_LOGIN_TOKEN'].encode()
LOGIN_VERIFICATION_MESSAGE = b'password verified'

print(f'SALT: {SALT}')
print(f'LOGIN_TOKEN: {LOGIN_TOKEN}')
