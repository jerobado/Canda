
import subprocess
from string import Template


_template = """Account: $account
Username: $username
Password: $password
"""


def get_unique_pc_identifier():
    """ Get and return computer's BIOS serialnumber. """

    args = ['wmic', 'bios', 'get', 'serialnumber']
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout.strip('SerialNumber\n ')


DETAILS_TEMPLATE = Template(_template)
RECORDS = []
LOGIN_VERIFICATION_MESSAGE = b'password verified'           # [] TODO: use different message
ACCOUNT_NAME = get_unique_pc_identifier()                   # for production
# ACCOUNT_NAME = '5'                                        # for development
INITIAL_RUN = True
