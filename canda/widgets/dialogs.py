# Create dialogs here

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog,
                             QLineEdit,
                             QLabel,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGridLayout,
                             QListView,
                             QListWidget,
                             QTextEdit,
                             QPushButton,
                             QMessageBox)


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

        self.setWindowTitle(f'Login - Canda {__version__}')
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
        self.questionMessageBox = QMessageBox()

    def _properties(self):

        self.setWindowTitle(f'Password Manager - Canda {__version__}')
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
        # self.recordListWidget.currentRowChanged.connect(self.on_recordListWidget_itemClicked) # [] TODO: review effect on deletePushButton
        self.addPushButton.clicked.connect(self.on_addPushButton_clicked)
        self.updatePushButton.clicked.connect(self.on_updatePushButton_clicked)
        self.deletePushButton.clicked.connect(self.on_deletePushButton_clicked)

    def on_recordListWidget_itemClicked(self):

        # To display the details of the selected item
        current_row = self.recordListWidget.currentRow()
        selected_record_dict = constant.RECORDS[current_row]
        result = constant.DETAILS_TEMPLATE.substitute(selected_record_dict)
        self.detailsTextEdit.setPlainText(result)

        # To enable the Delete button
        if not self.deletePushButton.isEnabled():
            self.deletePushButton.setEnabled(True)


    def on_addPushButton_clicked(self):

        # [] TODO: after adding, the current selection should point to the latest item
        dialog = AddDialog()
        if dialog.exec() == AddDialog.Accepted:

            username = dialog.usernameLineEdit.text()
            password = dialog.passwordLineEdit.text()
            account = dialog.accountLineEdit.text()

            new_record = canda.add_record(username=username,
                                          password=password,
                                          account=account)
            constant.RECORDS.append(new_record)

            insert_at = len(constant.RECORDS) - 1
            indentifier = constant.RECORDS[insert_at]['account']
            self.recordListWidget.insertItem(insert_at, indentifier)
            self.recordListWidget.setCurrentRow(insert_at)

    def on_updatePushButton_clicked(self):

        print('update')

    def on_deletePushButton_clicked(self):

        current_row = self.recordListWidget.currentRow()
        current_record = constant.RECORDS[current_row]
        message = f'Do you want to delete {current_record}?'
        result = QMessageBox.question(self, 'Before you do that...', message)

        # If the user hit Yes
        if result == 16384:
            deleted_record = canda.remove_record(current_row, constant.RECORDS)
            self.recordListWidget.takeItem(current_row)
            print(f'{deleted_record} deleted.')

        # Disable the Delete button if the record list hits zero
        if self.recordListWidget.count() == 0:
            self.deletePushButton.setEnabled(False)

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

        self.usernameLabel = QLabel('&Username')
        self.passwordLabel = QLabel('&Password')
        self.accountLabel = QLabel('A&ccount')
        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.accountLineEdit = QLineEdit()
        self.addPushButton = QPushButton()

    def _properties(self):

        self.usernameLineEdit.setObjectName('usernameLineEdit')

        self.usernameLabel.setBuddy(self.usernameLineEdit)

        self.passwordLabel.setBuddy(self.passwordLineEdit)

        self.passwordLineEdit.setObjectName('passwordLineEdit')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.accountLineEdit.setObjectName('accountLineEdit')

        self.accountLabel.setBuddy(self.accountLineEdit)

        self.addPushButton.setText('&Add')
        self.addPushButton.setEnabled(False)

        self.setObjectName('AddDialog')
        self.setWindowTitle('Add record - Canda')
        self.resize(327, 123)

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

        # [] TODO: change this to grid layout
        grid = QGridLayout()
        grid.addWidget(self.usernameLabel, 0, 0)
        grid.addWidget(self.usernameLineEdit, 0, 1)
        grid.addWidget(self.passwordLabel, 1, 0)
        grid.addWidget(self.passwordLineEdit, 1, 1)
        grid.addWidget(self.accountLabel, 2, 0)
        grid.addWidget(self.accountLineEdit, 2, 1)

        col_widgets = QVBoxLayout()
        col_widgets.addLayout(grid)
        col_widgets.addLayout(row_button)

        # self.setLayout(grid)
        self.setLayout(col_widgets)

    def resizeEvent(self, event):

        print(f'{self.objectName()}: {self.width()} x {self.height()}')

    def _connections(self):

        self.addPushButton.clicked.connect(self.accept)
        self.usernameLineEdit.textChanged.connect(self.on_LineEdits_textChanged)
        self.passwordLineEdit.textChanged.connect(self.on_LineEdits_textChanged)
        self.accountLineEdit.textChanged.connect(self.on_LineEdits_textChanged)

    def on_LineEdits_textChanged(self):

        sender = self.sender()
        print(sender.objectName())

        with_text = [self.usernameLineEdit.text(), self.passwordLineEdit.text(), self.accountLineEdit.text()]

        if all(with_text):
            print(with_text)
            self.addPushButton.setEnabled(True)
        else:
            self.addPushButton.setEnabled(False)
