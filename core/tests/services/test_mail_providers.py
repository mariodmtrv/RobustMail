__author__ = 'mariodimitrov'

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from core.services.mailgun_provider import MailGunProvider
from core.services.sendgrid_provider import SendgridProvider
from core.tests.services.testing_data import good_message_single_recipient, bad_message_wrong_address, unicode_message, \
    no_recipient_has_cc_bcc, no_content_message


class MailgunProviderTestCase(unittest.TestCase):
    def test_mailgun_sending_fails_wrong_address(self):
        m = bad_message_wrong_address()
        mailgun = MailGunProvider()
        self.assertEqual(mailgun.send_message(m), False)

    def test_simple_sending_successful(self):
        m = good_message_single_recipient()
        mailgun = MailGunProvider()
        self.assertEqual(mailgun.send_message(m), True)

    def test_unicode_message(self):
        m = unicode_message()
        mailgun = MailGunProvider()
        self.assertEqual(mailgun.send_message(m), True)

    def test_no_recipient_has_cc_bcc(self):
        m = no_recipient_has_cc_bcc()
        mailgun = MailGunProvider()
        self.assertEqual(mailgun.send_message(m), False)

    def test_no_content(self):
        m = no_content_message()
        mailgun = MailGunProvider()
        self.assertEqual(mailgun.send_message(m), False)


class SendgridProviderTestCase(unittest.TestCase):
    def test_sending_fails_wrong_address(self):
        """
        Accepts the message for queueing, drops it later
        """
        m = bad_message_wrong_address()
        sendgrid = SendgridProvider()
        self.assertEqual(sendgrid.send_message(m), True)

    def test_simple_sending_successful(self):
        m = good_message_single_recipient()
        sendgrid = SendgridProvider()
        self.assertEqual(sendgrid.send_message(m), True)

    def test_unicode_message(self):
        m = unicode_message()
        sendgrid = SendgridProvider()
        self.assertEqual(sendgrid.send_message(m), True)

    def test_no_recipient_has_cc_bcc(self):
        m = no_recipient_has_cc_bcc()
        sendgrid = SendgridProvider()
        self.assertEqual(sendgrid.send_message(m), False)

    def test_no_content(self):
        m = no_content_message()
        sendgrid = SendgridProvider()
        self.assertEqual(sendgrid.send_message(m), False)


if __name__ == '__main__':
    unittest.main()
