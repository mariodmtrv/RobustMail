__author__ = 'mariodimitrov'
from core.services.mail_provider import *
import sendgrid
from settings import SETTINGS
from core.mail.message import Message
from core.services.exceptions import ServiceDownException
import logging


class SendgridProvider(MailProvider):
    """
    Mail provider implementation for the Sendgrid service
    https://sendgrid.com/docs/API_Reference/Web_API/mail.html
    """

    @property
    def name(self):
        return self.__name

    def __init__(self):
        self.__name = "SendGrid"

    client = sendgrid.SendGridClient(SETTINGS["SENDGRID_USERNAME"], SETTINGS["SENDGRID_PASSWORD"])

    def to_sendgrid(self, message):
        result_message = sendgrid.Mail()
        result_message.set_from(message.sender.email)
        result_message.set_from_name(message.sender.name)
        result_message.set_subject(message.subject)
        result_message.set_text(message.text)
        for recipient in message.get_recipients():
            result_message.add_to(recipient.email)
            result_message.add_to_name(recipient.name)
        for cc_recipient in message.get_cc():
            result_message.add_cc(cc_recipient.email)
        for bcc_recipient in message.get_bcc():
            result_message.add_bcc(bcc_recipient.email)
        return result_message

    def send_message(self, message):
        result_message = self.to_sendgrid(message)
        result = self.client.send(result_message)
        if result[0] == 200:
            return True
        elif result[0] in range(400, 500):
            logging.error("Sending message with Sendgrid failed " + str(result[1]))
            return False
        elif result[0] >= 500:
            raise ServiceDownException("Sendgrid service failure " + str(result[1]))
            return False

    def get_delivery_status(self, message):
        raise NotImplementedError
