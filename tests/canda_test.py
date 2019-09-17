import sys
import unittest

from PyQt5.QtWidgets import QLineEdit, QApplication


APP = QApplication(sys.argv)


class CandaTest(unittest.TestCase):

    def setUp(self) -> None:
        from canda.main import LoginDialog
        self.login_dialog = LoginDialog()
        self.login_dialog.show()
        APP.exec()

    def test_loginLineEdit_echomode(self):
        """ Test if loginLineEdit's echomode is QLineEdit.Password or equal to 2 """

        test_result = self.login_dialog.loginLineEdit.echoMode()
        expected_result = QLineEdit.Password
        print(f'test_result {test_result}')
        print(f'expected_result {expected_result}')
        self.assertEqual(expected_result, test_result)  # result should be equal to 2

    def test_verify_function(self):
        """ Test if LoginDialog.verify() will return true if login credential is equal to 'masterkey' """

        test_result = self.login_dialog.loginLineEdit.text()
        expected_result = self.login_dialog.verify(test_result)
        print(f'test_result: {test_result}')
        print(f'expected_result {expected_result}')
        self.assertTrue(expected_result, test_result)


if __name__ == '__main__':
    unittest.main()
