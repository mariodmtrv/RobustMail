__author__ = 'mariodimitrov'

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from core.services.mailgun_provider import MailGunProvider
from core.services.sendgrid_provider import SendgridProvider
from core.tests.services.testing_data import good_message, bad_message_wrong_address


class MailgunProviderTestCase(unittest.TestCase):
    def test_mailgun_sending_fails_wrong_address(self):
        m = bad_message_wrong_address()
        mailgun = MailGunProvider()
        self.assertEqual(mailgun.send_message(m), False)

    @unittest.skip("Actual message sending")
    def test_simple_sending_successful(self):
        m = good_message()
        mailgun = MailGunProvider()
        self.assertEqual(mailgun.send_message(m), True)


class SendgridProviderTestCase(unittest.TestCase):
    def test_sending_fails_wrong_address(self):
        """
        Accepts the message for queueing, drops it later
        """
        m = bad_message_wrong_address()
        sendgrid = SendgridProvider()
        self.assertEqual(sendgrid.send_message(m), True)

    @unittest.skip("Actual message sending")
    def test_simple_sending_successful(self):
        m = good_message()
        sendgrid = SendgridProvider()
        self.assertEqual(sendgrid.send_message(m), True)


if __name__ == '__main__':
    unittest.main()
