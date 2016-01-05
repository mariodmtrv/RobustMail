__author__ = 'mariodimitrov'


class ServiceDownException(Exception):
    """
    When a message provider responded with server error
    """

    def __init__(self, message):
        super(ServiceDownException, self).__init__(message)
