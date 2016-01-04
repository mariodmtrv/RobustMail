__author__ = 'mariodimitrov'


class ServiceDownException(Exception):
    def __init__(self, message):
        super(ServiceDownException, self).__init__(message)
