try:
    import unittest2 as unittest
except ImportError:
    import unittest

from nose.tools import eq_

from core.services.message_service import create_message_service, send_message, revive_provider
from core.tests.services.testing_data import good_message_single_recipient, DummyMailProvider


class ServiceTestCase(unittest.TestCase):
    def test_send_message_successful(self):
        service = create_message_service()
        message = good_message_single_recipient()
        message.subject = "From robust provider test"
        result = send_message.apply(args=(service, message)).get()
        eq_(result, True)

    def test_primary_provider_failure(self):
        service = create_message_service()
        service.add_provider(DummyMailProvider())
        service.kill_provider(0)
        service.kill_provider(1)
        message = good_message_single_recipient()
        result = send_message.apply(args=(service, message)).get()
        eq_(result, True)

    @unittest.skip
    def test_retry_after_full_failure(self):
        service = create_message_service()
        service.kill_provider(0)
        service.kill_provider(1)
        revive_provider.apply(args=(service, 0), countdown=5)
        email = good_message_single_recipient()
        result = send_message.apply(args=(service, email)).get()
        eq_(result, True)


if __name__ == '__main__':
    unittest.main()
