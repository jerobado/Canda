# Create dialogs here

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog,
                             QLineEdit,
                             QLabel,
                             QVBoxLayout,
                             QHBoxLayout,
                             QListView,
                             QListWidget,
                             QTextEdit,
                             QPushButton)


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
        self.buttonsLabel = QLabel()
        self.recordListWidget = QListWidget()
        self.detailsTextEdit = QTextEdit()
        self.addPushButton = QPushButton()
        self.updatePushButton = QPushButton()
        self.deletePushButton = QPushButton()

    def _properties(self):

        self.setWindowTitle('Canda - Password Manager')
        self.setObjectName('MainDialog')

        self.recordLabel.setText('Records:')
        self.recordLabel.setObjectName('recordLabel')

        self.recordListWidget.setObjectName('recordListView')
        # self.recordListWidget.insertItems(0, constant.RECORDS)  # [] TODO: use QListView

        # TEST: inserting using for loop
        for index, value in enumerate(constant.RECORDS):
            self.recordListWidget.insertItem(index, constant.RECORDS[index]['account'])

        self.detailsLabel.setText('Details:')
        self.detailsLabel.setObjectName('detailsLabel')

        self.detailsTextEdit.setObjectName('detailsTextEdit')

        self.addPushButton.setObjectName('addPushButton')
        self.addPushButton.setText('&Add')

        self.updatePushButton.setObjectName('updatePushButton')
        self.updatePushButton.setText('&Update')
        self.updatePushButton.setEnabled(False)

        self.deletePushButton.setObjectName('deletePushButton')
        self.deletePushButton.setText('&Delete')
        self.deletePushButton.setEnabled(False)

    def _layouts(self):

        records_col = QVBoxLayout()
        records_col.addWidget(self.recordLabel)
        records_col.addWidget(self.recordListWidget)

        details_col = QVBoxLayout()
        details_col.addWidget(self.detailsLabel)
        details_col.addWidget(self.detailsTextEdit)

        buttons_col = QVBoxLayout()
        buttons_col.addWidget(self.buttonsLabel)    # filler widget
        buttons_col.addWidget(self.addPushButton)
        buttons_col.addWidget(self.updatePushButton)
        buttons_col.addWidget(self.deletePushButton)
        buttons_col.addStretch()

        combined_row = QHBoxLayout()
        combined_row.addLayout(records_col)
        combined_row.addLayout(details_col)
        combined_row.addLayout(buttons_col)

        self.setLayout(combined_row)

    def _connections(self):

        self.recordListWidget.itemClicked.connect(self.on_recordListWidget_itemClicked)
        self.addPushButton.clicked.connect(self.on_addPushButton_clicked)
        self.updatePushButton.clicked.connect(self.on_updatePushButton_clicked)
        self.deletePushButton.clicked.connect(self.on_deletePushButton_clicked)

    def on_recordListWidget_itemClicked(self):

        current_row = self.recordListWidget.currentRow()
        selected_record_dict = constant.RECORDS[current_row]
        result = constant.DETAILS_TEMPLATE.substitute(selected_record_dict)

        self.detailsTextEdit.setPlainText(result)

    def on_addPushButton_clicked(self):

        dialog = AddDialog()
        if dialog.exec() == AddDialog.Accepted:
            new_record = canda.add_record(username='alcoholuser',
                                          password='RheaBrand2222',
                                          account='Healthway')
            constant.RECORDS.append(new_record)

            insert_at = len(constant.RECORDS) - 1
            indentifier = constant.RECORDS[insert_at]['account']
            self.recordListWidget.insertItem(insert_at, indentifier)

    def on_updatePushButton_clicked(self):

        print('update')

    def on_deletePushButton_clicked(self):

        print('delete')

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()


class AddDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.usernameLabel = QLabel()
        self.passwordLabel = QLabel()
        self.accountLabel = QLabel()
        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.accountLineEdit = QLineEdit()
        self.addPushButton = QPushButton()

    def _properties(self):

        self.usernameLabel.setText('Username:')
        self.passwordLabel.setText('Password:')
        self.accountLabel.setText('Account:')

        self.addPushButton.setText('&Add')

        self.setWindowTitle('Add record - Canda')

    def _layouts(self):

        row_username = QHBoxLayout()
        row_username.addWidget(self.usernameLabel)
        row_username.addWidget(self.usernameLineEdit)

        row_password = QHBoxLayout()
        row_password.addWidget(self.passwordLabel)
        row_password.addWidget(self.passwordLineEdit)

        row_account = QHBoxLayout()
        row_account.addWidget(self.accountLabel)
        row_account.addWidget(self.accountLineEdit)

        row_button = QHBoxLayout()
        row_button.addStretch()
        row_button.addWidget(self.addPushButton)

        col_widgets = QVBoxLayout()
        col_widgets.addLayout(row_username)
        col_widgets.addLayout(row_password)
        col_widgets.addLayout(row_account)
        col_widgets.addLayout(row_button)

        self.setLayout(col_widgets)

    def _connections(self):

        self.addPushButton.clicked.connect(self.accept)
