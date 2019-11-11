""" Core operation of Canda """

import os
import sys
from canda.data.constant import (LOGIN_VERIFICATION_MESSAGE)


__version__ = 0.1


def _master_key():

    # [] TODO: think how and where to retrieve the masterkey in a secure place

    return 'masterkey'


def login(key):

    if key == MASTER_KEY:
        return True
    else:
        return False


def login3(key, salt, token):
    """ Test """

    try:
        import base64
        from cryptography.fernet import Fernet
        from cryptography.fernet import InvalidToken
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

        password = key.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                         length=32,
                         salt=salt,
                         iterations=100000,
                         backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        message = f.decrypt(token)

        if message == LOGIN_VERIFICATION_MESSAGE:
            return True

    except InvalidToken:
        print('Invalid Token: password unverified, try again')
        return False


def add_record(username, password, account):

    return {'username': username, 'password': password, 'account': account}


def update_record(record, **kwargs):
    """ Return the updated record based on the given **kwargs """

    record.update(kwargs)
    return record


def remove_record(index, record):
    """ Returns removed item in the record at the given index """

    return record.pop(index)


# [] TODO: for deletion, check other usage
def set_masterkey(key):

    return key


def set_masterkey3(key):
    """ Test function to set default masterkey

        Return key, salt, token
    """

    import base64
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    # for setting up new password
    password = key.encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = f.encrypt(LOGIN_VERIFICATION_MESSAGE)
    return key, salt, token


def get_platform():
    """ Get the underlying operating system. """

    return sys.platform


def get_bios_version_args():
    """ Get os specific commands to show the BIOS serial number. """

    args = None

    if sys.platform.startswith('win32'):
        args = ['wmic', 'bios', 'get', 'serialnumber']
    elif sys.platform.startswith('linux'):
        # [] TODO: add commands for Linux
        args = ['dmidecode', '-s', 'bios-version']

    return args


# [] TODO: for deletion, check other usage
MASTER_KEY = _master_key()
