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
        self.assertEqual(result, expected, 'discrepancy in masterkey ')

    def test_login_function_return_true(self):
        """ Test if login function returns True if 'masterkey' matches """

        result = self.canda.login('masterkey')
        self.assertTrue(result)

    def test_login_function_return_false(self):
        """ Test if login function returns False if 'masterkey' does not match """

        result = self.canda.login('xxx')
        self.assertFalse(result)

    def test_set_masterkey_function_return_equal(self):
        """ Test if set_masterkey(key) will change the default masterkey """

        result = self.canda.set_masterkey('freshmasterkey')
        expected = 'freshmasterkey'
        self.assertEqual(result, expected)

    def test_add_record_function_return_dict(self):
        """ Test if add_record will return a dictionary """

        result = self.canda.add_record(username='alcoholuser',
                                       password='RheaBrand2222',
                                       account='Healthway')
        expected = {'username': 'alcoholuser',
                    'password': 'RheaBrand2222',
                    'account': 'Healthway'}
        self.assertDictEqual(result, expected)

    def test_remove_record_function_return_dict(self):
        """ Test if remove_record will return the deleted item in the list """

        SAMPLE_LIST = [{'username': 'pixie@gmail.com', 'password': 'helloworld1234', 'account': 'GMail'},
                       {'username': 'hungrypoet_32@yahoo.com', 'password': 'novels111', 'account': 'Yahoo'},
                       {'username': 'blandsword@microsoft.com', 'password': 'helloworld1234', 'account': 'Microsoft'}]

        result = self.canda.remove_record(1, SAMPLE_LIST)
        expected = {'username': 'hungrypoet_32@yahoo.com',
                    'password': 'novels111',
                    'account': 'Yahoo'}
        self.assertDictEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
