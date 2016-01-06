__author__ = 'mariodimitrov'
from core.mail.email_validator import EmailValidator
from string import Template


class EmailUser:
    """
    Represents a participant in email conversation - sender or recipient
    """

    def __init__(self, email, name=''):
        self.__email = email
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    def __repr__(self):
        if self.__name is not '':
            return self.__name + " <" + self.__email + ">"
        return self.__email

    def __eq__(self, other):
        if self.__email == other.__email:
            return self.__name == other.__name
        return self.__email == other.__email


class Message():
    """
    Represents a message
    """

    def __init__(self):
        """
        Create a message
        """
        self.__sender = None
        self.__recipients = []
        self.__subject = ""
        self.__text = ""
        self.__options = {}
        self.__body = ""
        self.__cc = []
        self.__bcc = []

    def simple_message(self, sender_email, recipient_email, text, subject="", sender_name="", recipient_name=""):
        """
        Create a simple text message to a single recipient
        """
        self.set_sender(EmailUser(sender_email, sender_name))
        self.add_recipient(recipient_email, recipient_name)
        self.text = text
        self.subject = subject

    @property
    def sender(self):
        return self.__sender

    def set_sender(self, email, name=''):
        self.__sender = EmailUser(email, name)

    def add_recipient(self, email, name=''):
        self.__recipients.append(EmailUser(email, name))

    def get_recipients(self):
        return self.__recipients

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = subject

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    def add_option(self, name, value):
        """
        Add a custom message option and its value
        :param name: string The option name
        """
        self.__options[name] = value

    def get_option(self, name):
        """
        :param name: string Name of the option
        :return None if the option does not exists
        """
        if name in self.__options:
            return self.__options[name]
        return None

    def set_template_body(self, template_string, **content):
        """
        Create a rich text body using a template
        :param template_string:string: A parameterized body message
                Mark replaceable strings with $var_name
        :param content: dict: A dict with replaceable values
        """
        t = Template(template_string)
        self.__body = t.substitute(content)

    def get_cc(self):
        return self.__cc

    def get_bcc(self):
        return self.__bcc

    def add_cc(self, email, name=''):
        """
        Add a carbon copy recipient to the message
        """
        rec = EmailUser(email, name)
        self.__cc.append(rec)

    def add_bcc(self, email, name=''):
        rec = EmailUser(email, name)
        self.__bcc.append(rec)

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, body):
        self.__body = body

    def __is_valid_recipients(self):
        """
        :return: True if all recipient email addresses are syntactically correct
                False, otherwise
        """
        for recipient in self.__recipients:
            if not EmailValidator.is_syntax_valid(recipient.email):
                return False
        for recipient in self.__cc:
            if not EmailValidator.is_syntax_valid(recipient.email):
                return False
        for recipient in self.__bcc:
            if not EmailValidator.is_syntax_valid(recipient.email):
                return False
        return True

    def validate(self):
        """
        Validates a message for syntactic correctness
        :return: A tuple with boolean validation value and validation text result
                 If a validation failed the first failed check will be returned
        """
        if len(self.__recipients) == 0:
            return (False, "No recipients added")
        if self.text == "" and self.body == "":
            return (False, "Text or body is required")

        if not EmailValidator.is_syntax_valid(self.__sender.email):
            return (False, "Sender email invalid")
        if not self.__is_valid_recipients():
            return (False, "One or more recipient addresses incorrect")
        if self.subject == "":
            return (True, "Adding a subject is recommended")
        return (True, "Success")
