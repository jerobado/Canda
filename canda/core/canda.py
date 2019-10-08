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


def add_record(username, password, account):

    return {'username': username, 'password': password, 'account': account}


def remove_record(index, record):
    """ Returns removed item in the record at the given index """

    return record.pop(index)


def set_masterkey(key):

    return key


MASTER_KEY = _master_key()



