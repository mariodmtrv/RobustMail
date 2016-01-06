__author__ = 'mariodimitrov'
from abc import ABCMeta, abstractmethod
from core.mail.message import Message
from json import JSONEncoder


class MailProvider(metaclass=ABCMeta):
    """
    Represents an abstract mail provider
    """

    def send_message(self, message):
        """
        :param message:
        Sends a message to the required recipient/s
        :return True if message was queued successfully
                False if there was an issue
        :except ServiceDownException
        """

    @abstractmethod
    def get_delivery_status(self, message):
        """
        :param message: Message
        :return: the status of message delivery from the provider
        """
        pass

    @property
    @abstractmethod
    def name(self):
        return self.__name
