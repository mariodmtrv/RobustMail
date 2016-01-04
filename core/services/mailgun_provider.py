__author__ = 'mariodimitrov'
from core.services.mail_provider import *
from core.services.exceptions import ServiceDownException
from core.mail.message import Message
import requests
from settings import SETTINGS
import logging
import json


class MailGunProvider(MailProvider):
    """
Mail provider implementation for the MailGun service
https://documentation.mailgun.com/quickstart.html
"""

    @property
    def name(self):
        return self.__name

    def __init__(self):
        self.__name = "MailGun"

    @staticmethod
    def generate_recipients_list(recipients):
        result = []
        if recipients is not None:
            for rec in recipients:
                if rec is not None:
                    result.append(str(rec))
        return result

    def __manage_status_codes(self, request):
        if request.status_code == 200:
            return True
        elif request.status_code in range(300, 500):
            """
            TODO: Add better response for these status codes - wrong API key won't fix itself
            """
            logging.error("Sending message with Mailgun failed due to" + str(request.content))
            return False
        if request.status_code >= 500:
            raise ServiceDownException("Mailgun service failure " + str(request.content))

    def send_message(self, message):
        # As per https://documentation.mailgun.com/api-intro.html#errors
        recipients = self.generate_recipients_list(message.get_recipients())
        cc = self.generate_recipients_list(message.get_cc())
        bcc = self.generate_recipients_list(message.get_bcc())
        request = requests.post("https://api.mailgun.net/v3/" + SETTINGS["MAILGUN_BASE_URL"] + '/messages',
                                auth=("api", SETTINGS["MAILGUN_APIKEY"]),
                                data={"from": str(message.sender),
                                      "to": recipients,
                                      "cc": cc,
                                      "bcc": bcc,
                                      "subject": message.subject,
                                      "text": message.text,
                                      "html": message.body})
        return self.__manage_status_codes(request)

    def get_delivery_status(self, message):
        raise NotImplementedError
