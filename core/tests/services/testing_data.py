from core.mail.message import Message
from core.services.mail_provider import MailProvider
from core.services.exceptions import ServiceDownException


# TODO Replace recipient with a noreply mailbox
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


def good_message_single_recipient():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    m.add_recipient('mario.dimitrov@ymail.com', 'Regular Richtext Recipient')
    m.subject = "Very important"
    m.text = "Another spam message"
    m.body = "<h2> Very important for you </h2>"
    return m


def unicode_message():
    m = Message()
    m.set_sender('user@domain.com', 'Изпращач')
    m.add_recipient('mario.dimitrov@ymail.com', 'Марио Димитров')
    m.subject = "முக்கியமான செய்தி"
    m.text = "你好邮件服务"
    return m


def no_recipient_has_cc_bcc():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    m.add_cc('mario.dimitrov@ymail.com', 'Mario Dimitrov')
    m.add_bcc('mario.dimitrov@ymail.com')
    m.text = "Just spam"
    return m


def no_recipients_message():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    m.subject = "Very important"
    m.text = "Another spam message"
    m.body = "<h2> Very important for you </h2>"
    return m


def no_content_message():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    m.subject = "Very important"
    m.add_recipient('other.userdomain.com', 'Regular Recipient')
    m.add_cc('mario.dimitrov@ymail.com', 'Mario Dimitrov')
    m.add_bcc('mario.dimitrov@ymail.com')
    return m
