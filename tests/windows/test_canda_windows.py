import sys
import unittest

from PyQt5.QtWidgets import QLineEdit, QApplication


APP = QApplication(sys.argv)


class CandaGUITest(unittest.TestCase):
    """ Testing only the GUI """

    def setUp(self) -> None:
        if sys.platform == 'win32':
            from canda.main import LoginDialog
            self.login_dialog = LoginDialog()
            self.login_dialog.show()
            APP.exec()
        else:
            print('running on non-windows environment')

    def test_dialog_windowtitle(self):
        self.assertEqual(self.login_dialog.windowTitle(), 'Canda 0.1')

    def test_loginLineEdit_echomode(self):
        """ Test if loginLineEdit's echomode is QLineEdit.Password or equal to 2 """

        test_result = self.login_dialog.loginLineEdit.echoMode()
        expected_result = QLineEdit.Password
        print(f'test_result {test_result}')
        print(f'expected_result {expected_result}')
        self.assertEqual(expected_result, test_result)  # result should be equal to 2

    def test_verify_function_true(self):
        """ Test if LoginDialog.verify() will return True if 'masterkey' matches. """

        test_result = self.login_dialog.loginLineEdit.text()
        expected_result = self.login_dialog.verify(test_result)
        print(f'test_result: {test_result}')
        print(f'expected_result {expected_result}')
        self.assertTrue(expected_result, test_result)

    def test_verify_function_false(self):
        """ Test if LoginDialog.verify will return False if 'masterkey' does not matched. """

        test_result = self.login_dialog.loginLineEdit.text()
        expected_result = self.login_dialog.verify(test_result)
        self.assertFalse(expected_result, test_result)


class CandaCoreTest(unittest.TestCase):
    """ Testing only canda.py """

    def setUp(self) -> None:
        from canda.core import canda
        self.canda = canda

    def test_MASTER_KEY_if_equal(self):
        """ Test if MASTER_KEY is equal to 'masterkey' """

        result = self.canda.MASTER_KEY
        expected = 'masterkey'
        self.assertEqual(expected, result, 'discrepancy in masterkey ')


if __name__ == '__main__':
    unittest.main()
