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


if __name__ == '__main__':
    unittest.main()
