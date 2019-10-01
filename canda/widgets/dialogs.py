# Create dialogs here

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog,
                             QLineEdit,
                             QLabel,
                             QVBoxLayout,
                             QHBoxLayout,
                             QListView,
                             QListWidget,
                             QTextEdit)


from canda import __version__
from canda.core import canda
from canda.data import constant


class LoginDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.masterkey = canda.MASTER_KEY
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

        verified = canda.login(unverified_key)
        if verified:
            print('Verified. Enjoy your day!')
            self.accept()
            return True
        else:
            self.loginLineEdit.clear()
            print('Master key does not match. Try again.')
            return False

    def resizeEvent(self, event):

        print(f'{self.width()} x {self.height()}')

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

        if event.key() == Qt.Key_Return:
            print('Validating key...')
            self.verify(self.loginLineEdit.text())


class MainDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.recordLabel = QLabel()
        self.detailsLabel = QLabel()
        self.recordListWidget = QListWidget()
        self.detailsTextEdit = QTextEdit()

    def _properties(self):

        self.setWindowTitle('Canada - Password Manager')
        self.setObjectName('MainDialog')

        self.recordLabel.setText('Records:')
        self.recordLabel.setObjectName('recordLabel')

        self.recordListWidget.setObjectName('recordListView')
        self.recordListWidget.insertItems(0, constant.RECORDS)  # [] TODO: use QListView

        self.detailsLabel.setText('Details:')
        self.detailsLabel.setObjectName('detailsLabel')

        self.detailsTextEdit.setObjectName('detailsTextEdit')

    def _layouts(self):

        records_col = QVBoxLayout()
        records_col.addWidget(self.recordLabel)
        records_col.addWidget(self.recordListWidget)

        details_col = QVBoxLayout()
        details_col.addWidget(self.detailsLabel)
        details_col.addWidget(self.detailsTextEdit)

        combined_row = QHBoxLayout()
        combined_row.addLayout(records_col)
        combined_row.addLayout(details_col)

        self.setLayout(combined_row)

    def _connections(self):

        ...
