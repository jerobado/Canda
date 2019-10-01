""" Core operation of Canda """

__version__ = 0.1


def _master_key():

    # [] TODO: think how and where to retrieve the masterkey in a secure place

    return 'masterkey'


def login(key):

    if key == MASTER_KEY:
        return True
    else:
        return False


def set_masterkey(key):

    return key


MASTER_KEY = _master_key()



