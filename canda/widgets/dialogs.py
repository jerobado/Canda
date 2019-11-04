# Create dialogs here

from PyQt5.QtCore import (Qt,
                          QSettings)
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
from canda.data.constant import ACCOUNT_NAME


# [] TODO: create a setup dialog that will initialize the masterkey
class SetupDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.settings = QSettings()
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.accountnameLabel = QLabel()
        self.masterkeyLabel = QLabel()
        self.confirmkeyLabel = QLabel()
        self.confirmationLabel = QLabel()

        self.accountnameLineEdit = QLineEdit()
        self.masterkeyLineEdit = QLineEdit()
        self.confirmkeyLineEdit = QLineEdit()

        self.setPushButton = QPushButton('&Set Account')

    def _properties(self):

        self.accountnameLabel.setObjectName('accountnameLabel')
        self.accountnameLabel.setText('Account name:')

        # [ ] TODO: potentially to be removed
        self.accountnameLabel.setEnabled(False)
        self.accountnameLineEdit.setEnabled(False)

        self.masterkeyLabel.setObjectName('masterkeyLabel')
        self.masterkeyLabel.setText('Master key:')

        self.masterkeyLineEdit.setObjectName('masterkeyLineEdit')
        self.masterkeyLineEdit.setPlaceholderText(' something hard to guess')
        self.masterkeyLineEdit.setEchoMode(QLineEdit.Password)

        self.confirmkeyLabel.setObjectName('confirmkeyLabel')
        self.confirmkeyLabel.setText('Confirm master key:')

        self.confirmkeyLineEdit.setObjectName('confirmkeyLineEdit')
        self.confirmkeyLineEdit.setPlaceholderText(' making sure to avoid typos')
        self.confirmkeyLineEdit.setEchoMode(QLineEdit.Password)

        self.setPushButton.setObjectName('setPushButton')
        self.setPushButton.setEnabled(False)

        self.setWindowTitle('Setup Canda')
        self.resize(426, 142)

    def _layouts(self):

        grid = QGridLayout()
        grid.addWidget(self.accountnameLabel, 0, 0)
        grid.addWidget(self.accountnameLineEdit, 0, 1)
        grid.addWidget(self.masterkeyLabel, 1, 0)
        grid.addWidget(self.masterkeyLineEdit, 1, 1)
        grid.addWidget(self.confirmkeyLabel, 2, 0)
        grid.addWidget(self.confirmkeyLineEdit, 2, 1)
        grid.addWidget(self.confirmationLabel, 3, 1)

        row_button = QHBoxLayout()
        row_button.addStretch()
        row_button.addWidget(self.setPushButton)

        col_layout = QVBoxLayout()
        col_layout.addLayout(grid)
        col_layout.addLayout(row_button)

        self.setLayout(col_layout)

    def _connections(self):

        self.accountnameLineEdit.textChanged.connect(self.on_LineEdits_textChanged)
        self.masterkeyLineEdit.textChanged.connect(self.on_LineEdits_textChanged)
        self.confirmkeyLineEdit.textChanged.connect(self.on_LineEdits_textChanged)
        self.setPushButton.clicked.connect(self.on_setPushButton_clicked)

    def on_LineEdits_textChanged(self):

        # if self.confirmationLabel.text(): self.confirmationLabel.clear()

        # Enable of disable Set button if either of the three QLineEdits has a values
        # with_text = [self.accountnameLineEdit.text(), self.masterkeyLineEdit.text(), self.confirmkeyLineEdit.text()]
        with_text = [self.masterkeyLineEdit.text(), self.confirmkeyLineEdit.text()]
        print(with_text)

        if all(with_text):
            self.setPushButton.setEnabled(True)
        else:
            self.setPushButton.setEnabled(False)

    def on_setPushButton_clicked(self):

        self.check_masterkey_typo()

    def check_masterkey_typo(self):

        # Check for master key typos before encrypting it
        if self.masterkeyLineEdit.text() == self.confirmkeyLineEdit.text():
            print('password match, you may now proceed in encrypting the master key')
            credentials = self.encrypt_user_credentials()
            self._write_settings(credentials)
            self.accept()
        else:
            self.confirmationLabel.setText('Master key does not match.')
            self.masterkeyLineEdit.setFocus(True)
            self.confirmkeyLineEdit.clear()
            self.setPushButton.setEnabled(False)

    def encrypt_user_credentials(self):
        """ Encrypt user inputted credentials.

            Return key, salt, token
        """

        return canda.set_masterkey3(self.masterkeyLineEdit.text())

    def _write_settings(self, data):
        """ Save encrypted credentials to QSettings. """

        # self.settings = QSettings()
        print(f'on _write_settings: {self.settings.allKeys()}')
        self.settings.setValue('SALT', data[1])
        self.settings.setValue('LOGIN_TOKEN', data[2])
        self.settings.setValue('INITIAL_RUN', False)
        self.settings.sync()
        print(self.objectName(), 'settings save.')

    def resizeEvent(self, QResizeEvent):

        print(f'{self.width()} x {self.height()}')


class LoginDialog(QDialog):

    def __init__(self, account_name='', unverifed_key='', parent=None):

        super().__init__(parent)
        self.masterkey = canda.MASTER_KEY
        self.settings = QSettings()
        self.UNVERIFIED_KEY = unverifed_key
        self.INITIAL_RUN = True
        self.SALT = None
        self.LOGIN_TOKEN = None

        # TEST: playing with QSettings`
        self._read_settings()
        # self._set_masterkey(self.UNVERIFIED_KEY)

        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _set_masterkey(self, key):
        """ Set default master key. """

        print(self.INITIAL_RUN)
        if self.INITIAL_RUN:
            print('first setup of masterkey')
            # credentials = canda.set_masterkey3('defaultkeyx')
            credentials = canda.set_masterkey3(key)
            self.SALT = credentials[1]
            self.LOGIN_TOKEN = credentials[2]
            self.INITIAL_RUN = False
            print(f'INTIAL_RUN: {self.INITIAL_RUN}')
        else:
            print('you can use the masterkey you previously use')

    def _read_settings(self):
        """ Get restored last application settings. """

        self.SALT = self.settings.value('SALT', self.SALT)
        self.LOGIN_TOKEN = self.settings.value('LOGIN_TOKEN', self.LOGIN_TOKEN)
        self.INITIAL_RUN = self.settings.value('INITIAL_RUN', self.INITIAL_RUN, bool)

        print('\non _read_settings() function')
        print(f'self.SALT: {self.SALT}')
        print(f'self.LOGIN_TOKEN: {self.LOGIN_TOKEN}')

    def _write_settings(self):
        """ Save new application settings. """

        self.settings.setValue('SALT', self.SALT)
        self.settings.setValue('LOGIN_TOKEN', self.LOGIN_TOKEN)
        self.settings.setValue('INITIAL_RUN', self.INITIAL_RUN)
        # self.settings.setValue('INITIAL_RUN', True)

    def _widgets(self):

        self.loginLabel = QLabel('Canda - Password Manager in the 21st Century')
        self.loginLineEdit = QLineEdit()
        self.setmasterkeyLabel = QLabel('<a href="https://python.org">Set Master Key</a>')

    def _properties(self):

        self.loginLineEdit.setPlaceholderText('Enter master key here')
        self.loginLineEdit.setEchoMode(QLineEdit.Password)
        self.setmasterkeyLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setmasterkeyLabel.setOpenExternalLinks(True)

        self.setWindowTitle(f'Login - Canda {__version__}')
        self.resize(402, 61)

    def _layouts(self):

        vbox = QVBoxLayout()
        vbox.addWidget(self.loginLabel)
        vbox.addWidget(self.loginLineEdit)
        vbox.addWidget(self.setmasterkeyLabel)

        self.setLayout(vbox)

    def _connections(self):

        self.loginLineEdit.textChanged.connect(self.on_loginLineEdit_textChanged)

    def on_loginLineEdit_textChanged(self):

        print(self.loginLineEdit.text())

    def verify(self, unverified_key):
        """ Verify master key. """

        # verified = canda.login(unverified_key)
        # verified = canda.login2(unverified_key)
        verified = canda.login3(unverified_key, self.SALT, self.LOGIN_TOKEN)
        if verified:
            print('Verified. Enjoy your day!')
            self.accept()
            return True
        else:
            self.loginLineEdit.clear()
            print('Master key does not match. Try again.')
            return False

    def hideEvent(self, *args, **kwargs):

        self._write_settings()

    def closeEvent(self, event):

        print('im closed')

    def resizeEvent(self, event):

        print(f'{self.width()} x {self.height()}')

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

        if event.key() == Qt.Key_Return:
            print('Validating key...')
            self.verify(self.loginLineEdit.text())
            # self.verify(self.UNVERIFIED_KEY)


class MainDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.settings = QSettings()
        self._read_settings()
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _read_settings(self):

        constant.RECORDS = self.settings.value('RECORDS', constant.RECORDS)

    def _write_settings(self):

        self.settings.setValue('RECORDS', constant.RECORDS)

    def _widgets(self):

        self.recordLabel = QLabel()
        self.detailsLabel = QLabel()
        self.buttonsLabel = QLabel()
        self.recordListWidget = QListWidget()
        self.detailsTextEdit = QTextEdit()
        self.addPushButton = QPushButton()
        self.updatePushButton = QPushButton()
        self.deletePushButton = QPushButton()
        self.setmasterkeyButton = QPushButton()
        self.questionMessageBox = QMessageBox()

    def _properties(self):

        self.setWindowTitle(f'Password Manager - Canda {__version__}')
        self.setObjectName('MainDialog')

        self.recordLabel.setText('Records:')
        self.recordLabel.setObjectName('recordLabel')

        self.recordListWidget.setObjectName('recordListView')
        # self.recordListWidget.insertItems(0, constant.RECORDS)  # [] TODO: use QListView

        # [] TODO: use QSettings here to retrieve the data from the last session
        if constant.RECORDS:
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

        self.setmasterkeyButton.setText('&Set Master Key')

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
        buttons_col.addWidget(self.setmasterkeyButton)
        buttons_col.addStretch()

        combined_row = QHBoxLayout()
        combined_row.addLayout(records_col)
        combined_row.addLayout(details_col)
        combined_row.addLayout(buttons_col)

        self.setLayout(combined_row)

    def _connections(self):

        self.recordListWidget.itemClicked.connect(self.on_recordListWidget_itemClicked)
        # self.recordListWidget.currentRowChanged.connect(self.on_recordListWidget_currentRowChanged) # tricky to use but with potential
        self.addPushButton.clicked.connect(self.on_addPushButton_clicked)
        self.updatePushButton.clicked.connect(self.on_updatePushButton_clicked)
        self.deletePushButton.clicked.connect(self.on_deletePushButton_clicked)
        self.setmasterkeyButton.clicked.connect(self.on_setmasterkeyPushButton_clicked)

    def on_recordListWidget_itemClicked(self):

        print('click at ', self.recordListWidget.currentRow())

        # To display the details of the selected item
        current_row = self.recordListWidget.currentRow()
        selected_record_dict = constant.RECORDS[current_row]
        result = constant.DETAILS_TEMPLATE.substitute(selected_record_dict)
        self.detailsTextEdit.setPlainText(result)

        # To enable the Update and Delete button
        if not self.deletePushButton.isEnabled() and not self.updatePushButton.isEnabled():
            self.updatePushButton.setEnabled(True)
            self.deletePushButton.setEnabled(True)

    def on_recordListWidget_currentRowChanged(self):

        ...

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

            # Update detailsTextEdit to reflect the current selected row
            new_current_row = self.recordListWidget.currentRow()
            new_selected_record = constant.RECORDS[new_current_row]
            result = constant.DETAILS_TEMPLATE.substitute(new_selected_record)
            self.detailsTextEdit.setPlainText(result)

            if not self.deletePushButton.isEnabled() and not self.updatePushButton.isEnabled():
                self.updatePushButton.setEnabled(True)
                self.deletePushButton.setEnabled(True)

    def on_updatePushButton_clicked(self):

        dialog = UpdateDialog()
        # get values of selected item
        current_row = self.recordListWidget.currentRow()
        current_record = constant.RECORDS[current_row]

        # display retrieved values to Update dialog
        dialog.usernameLineEdit.setText(current_record['username'])
        dialog.passwordLineEdit.setText(current_record['password'])
        dialog.accountLineEdit.setText(current_record['account'])

        if dialog.exec() == UpdateDialog.Accepted:
            new_record = {'username': dialog.usernameLineEdit.text(),
                          'password': dialog.passwordLineEdit.text(),
                          'account': dialog.accountLineEdit.text()}

            canda.update_record(current_record, **new_record)

            # Update detailsTextEdit to reflect the current selected row
            new_current_row = self.recordListWidget.currentRow()
            new_selected_record = constant.RECORDS[new_current_row]
            result = constant.DETAILS_TEMPLATE.substitute(new_selected_record)
            self.detailsTextEdit.setPlainText(result)

            # Don't like this but it works, to be refactored soon
            self.recordListWidget.clear()
            for index, value in enumerate(constant.RECORDS):
                self.recordListWidget.insertItem(index, constant.RECORDS[index]['account'])
            self.recordListWidget.setCurrentRow(new_current_row)

            print('updated')

    def on_deletePushButton_clicked(self):

        current_row = self.recordListWidget.currentRow()
        current_record = constant.RECORDS[current_row]
        message = f'Do you want to delete your account in \'{current_record["account"]}\'?'
        result = QMessageBox.question(self, 'Before you do that...', message)

        # If the user hit Yes
        if result == 16384:
            deleted_record = canda.remove_record(current_row, constant.RECORDS)
            self.recordListWidget.takeItem(current_row)
            print(f'{deleted_record} deleted.')

        # Update detailsTextEdit to reflect the current selected row as long as the recordList is not empty, -1 is empty
        if not self.recordListWidget.currentRow() == -1:
            new_current_row = self.recordListWidget.currentRow()
            new_selected_record = constant.RECORDS[new_current_row]
            result = constant.DETAILS_TEMPLATE.substitute(new_selected_record)
            self.detailsTextEdit.setPlainText(result)

        # Disable the Update and Delete buttons and clear the details text edit if the record list hits zero
        elif self.recordListWidget.count() == 0:
            self.updatePushButton.setEnabled(False)
            self.deletePushButton.setEnabled(False)
            self.detailsTextEdit.clear()

    def on_setmasterkeyPushButton_clicked(self):

        print('show Setup dialog')
        # show Setup dialog
        # show Login dialog
        setup = SetupDialog()
        if setup.exec() == SetupDialog.Accepted:

            login = LoginDialog(account_name=setup.accountnameLineEdit.text())
            login.setWindowTitle('Re-login')
            # login = LoginDialog(account_name=ACCOUNT_NAME)
            self.hide()
            if login.exec() == LoginDialog.Accepted:
                self.show()

    def closeEvent(self, event):

        self._write_settings()

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

        self.usernameLabel = QLabel('&Username:')
        self.passwordLabel = QLabel('&Password:')
        self.accountLabel = QLabel('A&ccount:')
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
        self.setWindowTitle('Add')
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


class UpdateDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.usernameLabel = QLabel('&Username:')
        self.passwordLabel = QLabel('&Password:')
        self.accountLabel = QLabel('A&ccount:')
        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.accountLineEdit = QLineEdit()
        self.updatePushButton = QPushButton()

    def _properties(self):

        self.usernameLineEdit.setObjectName('usernameLineEdit')

        self.usernameLabel.setBuddy(self.usernameLineEdit)

        self.passwordLabel.setBuddy(self.passwordLineEdit)

        self.passwordLineEdit.setObjectName('passwordLineEdit')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.accountLineEdit.setObjectName('accountLineEdit')

        self.accountLabel.setBuddy(self.accountLineEdit)

        self.updatePushButton.setText('&Update')
        self.updatePushButton.setEnabled(False)

        self.setObjectName('UpdateDialog')
        self.setWindowTitle('Update')
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
        row_button.addWidget(self.updatePushButton)

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

        self.updatePushButton.clicked.connect(self.accept)
        self.usernameLineEdit.textChanged.connect(self.on_LineEdits_textChanged)
        self.passwordLineEdit.textChanged.connect(self.on_LineEdits_textChanged)
        self.accountLineEdit.textChanged.connect(self.on_LineEdits_textChanged)

    def on_LineEdits_textChanged(self):

        sender = self.sender()
        print(sender.objectName())

        with_text = [self.usernameLineEdit.text(), self.passwordLineEdit.text(), self.accountLineEdit.text()]

        if all(with_text):
            print(with_text)
            self.updatePushButton.setEnabled(True)
        else:
            self.updatePushButton.setEnabled(False)
