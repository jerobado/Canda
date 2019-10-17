""" Core operation of Canda """

from canda.data.constant import LOGIN_TOKEN

__version__ = 0.1


def _master_key():

    # [] TODO: think how and where to retrieve the masterkey in a secure place

    return 'masterkey'


def login2(key):
    """ Test login using cryptography library """

    import base64
    import os
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
    token = f.encrypt(b'password verified')
    message = f.decrypt(token)
    print('login2 - message:', message)

    if message == b'password verified':
        return True
    else:
        return False


def login(key):

    if key == MASTER_KEY:
        return True
    else:
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


def set_masterkey(key):

    return key


MASTER_KEY = _master_key()



