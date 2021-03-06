
import subprocess
import sys
from string import Template
from canda.core import canda

_template = """Account: $account
Username: $username
Password: $password
"""


def get_unique_pc_identifier():
    """ Get and return computer's BIOS serialnumber. """

    # For Windows
    if sys.platform.startswith('win32'):
        args = ['wmic', 'bios', 'get', 'serialnumber']
    elif sys.platform.startswith('linux'):
        args = ['dmidecode', '-s', 'bios-version']

    # args = canda.get_bios_version_args()  # [] TODO: this one is crashing
    result = subprocess.run(args, capture_output=True, text=True)

    return result.stdout.strip('SerialNumber\n ')


DETAILS_TEMPLATE = Template(_template)
RECORDS = []
LOGIN_VERIFICATION_MESSAGE = b'password verified'           # [] TODO: use different message
ACCOUNT_NAME = get_unique_pc_identifier()                   # for production
# ACCOUNT_NAME = '7'                                        # for development
INITIAL_RUN = True
