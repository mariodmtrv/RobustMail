from core.mail.message import Message
from core.services.mail_provider import MailProvider
from core.services.exceptions import ServiceDownException


class DummyMailProvider(MailProvider):
    """
    A controllable provider for testing purposes
    """

    @property
    def name(self):
        return self.__name

    def __init__(self):
        self.__name = "DummyProvider"
        self.__alive = True

    def send_message(self, message):
        if self.__alive:
            return True
        raise ServiceDownException("Dummy provider is down")

    def flip_status(self):
        self.__alive = not self.__alive

    def get_delivery_status(self, message):
        raise NotImplementedError


def bad_message_wrong_address():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    m.add_recipient('other.userdomain.com', 'Regular Recipient')
    m.subject = "Very important"
    m.text = "Another spam message"
    return m


def good_message():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    # TODO Replace with a noreply mailbox
    m.add_recipient('mario.dimitrov@ymail.com', 'Regular Recipient')
    m.subject = "Very important"
    m.text = "Another spam message"
    return m
