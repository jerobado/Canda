""" Core operation of Canda """

from canda.data.constant import LOGIN_TOKEN
from canda.data.constant import SALT


__version__ = 0.1


def _master_key():

    # [] TODO: think how and where to retrieve the masterkey in a secure place

    return 'masterkey'


def login2(key):
    """ Test login using cryptography library """

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
                         salt=SALT,
                         iterations=100000,
                         backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        message = f.decrypt(LOGIN_TOKEN)
        print('login2 - message:', message)

        if message == b'password verified':
            print('holy @#$! we are now logging in using cryptography!')
            return True

    except InvalidToken:
        print('not your password')
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


def set_masterkey2(key):
    """ Using cryptography to set the masterkey """

    import base64
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    # for setting up new password
    password = key.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=SALT,
                     iterations=100000,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


MASTER_KEY = _master_key()



