# Create dialogs here

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog,
                             QLineEdit,
                             QLabel,
                             QVBoxLayout)

from canda import __version__


class LoginDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.masterkey = 'masterkey'
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.loginLabel = QLabel('Canda - Password Manager in the 21st Century')
        self.loginLineEdit = QLineEdit()

    def _properties(self):

        self.loginLineEdit.setPlaceholderText('Enter master key here')
        self.loginLineEdit.setEchoMode(QLineEdit.Password)

        self.setWindowTitle(f'Canda {__version__}')
        self.resize(402, 61)

    def _layouts(self):

        vbox = QVBoxLayout()
        vbox.addWidget(self.loginLabel)
        vbox.addWidget(self.loginLineEdit)

        self.setLayout(vbox)

    def _connections(self):

        self.loginLineEdit.textChanged.connect(self.on_loginLineEdit_textChanged)

    def on_loginLineEdit_textChanged(self):

        print(self.loginLineEdit.text())

    def verify(self, unverified_key):
        """ Verify master key. """

        if unverified_key == self.masterkey:
            print('Verified!')
            self.accept()
            return True
        else:
            print('Master key does not match. Try again.')
            return 0

    def resizeEvent(self, event):

        print(f'{self.width()} x {self.height()}')

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

        if event.key() == Qt.Key_Return:
            print('validating master key...')
            self.verify(self.loginLineEdit.text())


class MainDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        ...

    def _properties(self):

        self.setWindowTitle('Canada - Password Manager')

    def _layouts(self):

        ...

    def _connections(self):

        ...
