
from string import Template

_template = """Account: $account
Username: $username
Password: $password
"""

DETAILS_TEMPLATE = Template(_template)


RECORDS = [{'username': 'pixie@gmail.com', 'password': 'helloworld1234', 'account': 'GMail'},
           {'username': 'hungrypoet_32@yahoo.com', 'password': 'novels111', 'account': 'Yahoo'},
           {'username': 'blandsword@microsoft.com', 'password': 'helloworld1234', 'account': 'Microsoft'}]

