import sys
import unittest

from PyQt5.QtWidgets import QLineEdit, QApplication


class CandaDialogTest(unittest.TestCase):

    def setUp(self) -> None:
        if sys.platform == 'linux':
            from canda.main import LoginDialog
            APP = QApplication(sys.argv)
            self.login_dialog = LoginDialog()
            self.login_dialog.show()
            APP.exec()
        else:
            from canda.main import LoginDialog
            APP = QApplication(sys.argv)
            self.login_dialog = LoginDialog()
            self.login_dialog.show()
            APP.exec()

    def test_dialog_windowtitle(self):

        expected_result = 'Canda 0.1'
        test_result = self.login_dialog.windowTitle()
        self.assertEqual(test_result, expected_result)


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

    def test_login_function_return_true(self):
        """ Test if login function returns True if 'masterkey' matches """

        result = self.canda.login('masterkey')
        self.assertTrue(result)

    def test_login_function_return_false(self):
        """ Test if login function returns False if 'masterkey' does not match """

        result = self.canda.login('xxx')
        self.assertFalse(result)

    def test_get_bios_version_args(self):

        result = self.canda.get_bios_version_args()
        expected = ['dmidecode', '-s', 'bios-version']

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
