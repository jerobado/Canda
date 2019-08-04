"""
Canda is a desktop application password manager in the 21st century written and hand-coded in Python.

Benefits
* Easily retrieve login credentials of online accounts
* Secure saved login credentials in an encrypted database stored in your local machine
* Lock and unlock your password manager using a master password

"""


import sys
from PyQt5.QtWidgets import (QApplication,
                             QDialog,
                             QLineEdit,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout)


__version__ = 0.1


# create the login window
class LoginDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.loginLabel = QLabel('Canda - Password Manager in the 21st Century')
        self.loginLineEdit = QLineEdit()

    def _properties(self):

        self.loginLineEdit.setPlaceholderText('Enter master key here')

        self.setWindowTitle(f'Canda {__version__}')
        self.resize(402, 61)

    def _layouts(self):

        vbox = QVBoxLayout()
        vbox.addWidget(self.loginLabel)
        vbox.addWidget(self.loginLineEdit)

        self.setLayout(vbox)

    def _connections(self):

        ...

    def resizeEvent(self, event):

        print(f'{self.width()} x {self.height()}')


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    window = LoginDialog()
    window.show()
    APP.exec()
