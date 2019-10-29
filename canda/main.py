"""
Canda is a desktop application password manager in the 21st century written and hand-coded in Python.

Benefits
* Easily retrieve login credentials of online accounts
* Secure saved login credentials in an encrypted database stored in your local machine
* Lock and unlock your password manager using a master password

"""


import sys
from PyQt5.QtWidgets import QApplication

from canda.widgets.dialogs import (SetupDialog,
                                   LoginDialog,
                                   MainDialog)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    setup = SetupDialog()
    if setup.exec() == SetupDialog.Accepted:
        login = LoginDialog()
        if login.exec() == LoginDialog.Accepted:
            window = MainDialog()
            window.show()
            APP.exec()
