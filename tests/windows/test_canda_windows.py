import sys
import unittest

from PyQt5.QtWidgets import QLineEdit, QApplication


APP = QApplication(sys.argv)


# [] TODO: for possible deletion
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

    def test_update_record_updates_one_pair(self):
        """ Test if update_record will update the given dictionary """

        sample_record = {'username': 'alcoholuser',
                         'password': 'RheaBrand2222',
                         'account': 'Healthway'}

        sample_record2 = {'username': 'alcoholuser',
                          'password': 'RheaBrand2222',
                          'account': 'Healthway'}

        sample_record3 = {'username': 'alcoholuser',
                          'password': 'RheaBrand2222',
                          'account': 'Healthway'}

        sample_kwargs = {'username': 'new_alcoholuser'}

        sample_kwargs2 = {'username': 'new_alcoholuser',
                          'password': 'BrandedAlcohol'}

        sample_kwargs3 = {'username': 'never_new_alcoholuser',
                          'password': 'BrandedAlcohol',
                          'account': 'agos'}

        result = self.canda.update_record(sample_record, **sample_kwargs)
        result2 = self.canda.update_record(sample_record2, **sample_kwargs2)
        result3 = self.canda.update_record(sample_record3, **sample_kwargs3)

        expected = {'username': 'new_alcoholuser',
                    'password': 'RheaBrand2222',
                    'account': 'Healthway'}

        expected2 = {'username': 'new_alcoholuser',
                     'password': 'BrandedAlcohol',
                     'account': 'Healthway'}

        expected3 = {'username': 'never_new_alcoholuser',
                     'password': 'BrandedAlcohol',
                     'account': 'agos'}

        self.assertDictEqual(result, expected)
        self.assertDictEqual(result2, expected2)
        self.assertDictEqual(result3, expected3)

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

    def test_get_operating_system_windows(self):
        """ Test if get_platform() will return 'win32' """

        result = self.canda.get_platform()
        expected = 'win32'

        self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
