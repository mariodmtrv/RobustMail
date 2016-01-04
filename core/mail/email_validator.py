__author__ = 'mariodimitrov'

import re
import dns.resolver
import logging


class EmailValidator:
    """
Validates an email address
"""

    @staticmethod
    def is_syntax_valid(email):
        """
        Performs a simple format validation of a given email address
        :param email: string
        """
        return re.match(r"[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*\.[a-zA-Z0-9]{2,}", email)


    @staticmethod
    def is_mx_valid(email):
        """
        Performs an email validation whether an MX record exists
        :param email: string
        """
        try:
            domain = re.search("@[\w.]+", email).group()[1:]
            answers = dns.resolver.query(domain, 'MX')
            return True
        except dns.resolver.NXDOMAIN:
            # No MX record
            return False
        except:
            logging.error("Unexpected MX entry validation failure at EmailValidator")
            return False

    @staticmethod
    def is_valid(email):
        """
        Performs an email validation syntax-wise and whether an MX record exists
        :param email: string
        """
        if EmailValidator.is_syntax_valid(email):
            return EmailValidator.is_mx_valid(email)
        return False