""" Core operation of Canda """


def _master_key():

    # [] TODO: think how and where to retrieve the masterkey in a secure place

    return 'masterkey'


def login(key):

    if key == MASTER_KEY:
        return True
    else:
        return False


MASTER_KEY = _master_key()



