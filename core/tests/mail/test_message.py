__author__ = 'mariodimitrov'

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from core.mail.message import Message, EmailUser


class MessageTestCase(unittest.TestCase):
    def __create_message(self):
        m = Message()
        m.set_sender('user@domain.com', 'Regular Sender')
        m.add_recipient('other.user@domain.com', 'Regular Recipient')
        m.subject = "Very important"
        m.text = "Another spam message"
        return m

    def test_message_single_recipient(self):
        message = self.__create_message()
        actual_recs = message.get_recipients()
        self.assertListEqual(actual_recs, [EmailUser('other.user@domain.com', 'Regular Recipient')])
        self.assertEqual(message.subject, 'Very important')

    def test_message_multiple_recipients_multiple_types(self):
        message = self.__create_message()
        message.add_cc('cc.user@domain.com', 'Carbon Copier')
        message.add_bcc('bcc.user@domain.com')
        actual_bcc = message.get_bcc()
        self.assertListEqual(actual_bcc, [EmailUser('bcc.user@domain.com')])

    def test_simple_message_creation(self):
        message = Message()
        message.simple_message('user@domain.com', 'other.user@domain.com', 'Another spam message')
        self.assertEqual(message.text, 'Another spam message')

    def test_message_validation_all_correct(self):
        message = self.__create_message()
        result = message.validate()
        self.assertEqual("Success", result[1])

    def test_message_validation_no_content(self):
        message = self.__create_message()
        message.text = ""
        result = message.validate()
        self.assertEqual("Text or body is required", result[1])
