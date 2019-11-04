
import base64
import os
from string import Template

_template = """Account: $account
Username: $username
Password: $password
"""

DETAILS_TEMPLATE = Template(_template)
RECORDS = []
SALT = base64.b64decode(os.environ['CANDA_SALT'])           # [] TODO: to be deleted, check first
LOGIN_TOKEN = os.environ['CANDA_LOGIN_TOKEN'].encode()      # [] TODO: to be deleted, check first
LOGIN_VERIFICATION_MESSAGE = b'password verified'           # [] TODO: use different message
ACCOUNT_NAME = '5'                                          # [] TODO: use unique PC identifier
INITIAL_RUN = True
