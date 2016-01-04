__author__ = 'mariodimitrov'
from core.mail.email_validator import *

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class EmailValidatorTestCase(unittest.TestCase):
    def test_valid_address_domains(self):
        self.assertTrue(EmailValidator.is_valid("test@names.co.uk"))
        self.assertTrue(EmailValidator.is_valid("test.user@gmail.com"))
        self.assertTrue(EmailValidator.is_valid("test@abv.bg"))

    def test_invalid_address_domain(self):
        self.assertFalse(EmailValidator.is_valid("test@veryrandomstring.co.bg"))

    def test_syntax_invalid_addresses(self):
        self.assertFalse(EmailValidator.is_valid("test.ymail.com"))
        self.assertFalse(EmailValidator.is_valid("@ymail.com"))
        self.assertFalse(EmailValidator.is_valid("test@ymail"))


if __name__ == '__main__':
    unittest.main()
