__author__ = 'mariodimitrov'


class ServiceDownException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ServiceDownException, self).__init__(message)