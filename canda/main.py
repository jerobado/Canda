"""
Canda is a desktop application password manager in the 21st century written and hand-coded in Python.

Benefits
* Easily retrieve login credentials of online accounts
* Secure saved login credentials in an encrypted database stored in your local machine
* Lock and unlock your password manager using a master password
"""


import sys
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication
from canda.widgets.dialogs import (SetupDialog,
                                   LoginDialog,
                                   MainDialog)
from canda.data.constant import (ACCOUNT_NAME,
                                 INITIAL_RUN)


def without_masterkey():
    """ Run this if there is no master key yet setup. """

    APP = QApplication(sys.argv)
    setup = SetupDialog()
    if setup.exec() == SetupDialog.Accepted:
        login = LoginDialog(account_name=ACCOUNT_NAME)
        # login = LoginDialog()
        if login.exec() == LoginDialog.Accepted:
            window = MainDialog()
            window.show()
            APP.exec()


def with_masterkey():
    """ Run this if a master key is already setup. """

    APP = QApplication(sys.argv)
    login = LoginDialog(account_name=ACCOUNT_NAME)
    if login.exec() == LoginDialog.Accepted:
        window = MainDialog()
        window.show()
        APP.exec()


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    APP.setOrganizationName(ACCOUNT_NAME)
    APP.setApplicationName('Canda')

    settings = QSettings()
    INITIAL_RUN = settings.value('INITIAL_RUN', INITIAL_RUN, bool)

    if not INITIAL_RUN:
        with_masterkey()
    else:
        without_masterkey()
