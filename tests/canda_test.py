import sys
import unittest

from PyQt5.QtWidgets import QLineEdit, QApplication


APP = QApplication(sys.argv)


class CandaTest(unittest.TestCase):

    def setUp(self) -> None:
        from src.main import LoginDialog
        self.login_dialog = LoginDialog()
        self.login_dialog.show()
        APP.exec()

    def test_loginLineEdit_echomode(self):
        """ Test if loginLineEdit's echomode is QLineEdit.Password. """

        test_result = self.login_dialog.loginLineEdit.echoMode()
        expected_result = QLineEdit.Password
        self.assertTrue(expected_result, test_result)   # result is 2


if __name__ == '__main__':
    unittest.main()
