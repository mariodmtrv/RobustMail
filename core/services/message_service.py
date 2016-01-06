__author__ = 'mariodimitrov'
from core.services.mail_provider import MailProvider
from core.services.mailgun_provider import MailGunProvider
from core.services.sendgrid_provider import SendgridProvider
from celery.utils.log import get_task_logger
from settings import SETTINGS
from celery import Celery
from core.services.exceptions import ServiceDownException

logger = get_task_logger(__name__)


def make_celery():
    """
    Configures Celery task queue
    """
    celery = Celery("tasks", broker=SETTINGS['MESSAGE_BROKER_URL'],
                    backend=SETTINGS['REDIS_URL'])
    # Settings to adjust to the AMQP message quota
    celery.conf.update(
            CELERY_TASK_SERIALIZER='pickle',
            CELERY_ACCEPT_CONTENT=['pickle'],
            CELERY_RESULT_SERIALIZER='json',
            BROKER_POOL_LIMIT=1,
            CELERYD_CONCURRENCY=2,
            CELERYD_PROCESSES=1
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()


@celery.task(name="revive_provider")
def revive_provider(service, provider_ind):
    """
       Makes a provider in the service available for sending attempts
       :param provider_ind: Index of the provider
       """
    service.revive_provider(provider_ind)


@celery.task(bind=True, default_retry_delay=15, max_retries=3)
def send_message(self, service, email):
    """
    Sends a message with the first available provider
    In case it fails, attempts with the next one and sets a countdown when to try again with the failed one
    :param service: The message service that offers multiple providers
    :param email:The message
    :return: True if sending was successful, False if the provider did not accept it
    """
    provider_ind = 0
    for provider in service.providers:
        if service.is_available(provider_ind):
            try:
                result = provider.send_message(email)
                return result
            except ServiceDownException:
                service.kill_provider(provider_ind)
                revive_provider.apply_async(args=(service, provider_ind), countdown=15)
        provider_ind += 1
    if provider_ind >= len(service.providers):
        raise self.retry(exc=ServiceDownException("Services failed"))


class MessageService():
    def __init__(self):
        self.providers = []
        self.__provider_avail = []

    def add_provider(self, provider):
        """
        :param provider: MailProvider: An instance of MailProvider subclass
        """
        if provider is not None and isinstance(provider, MailProvider):
            self.providers.append(provider)
            self.__provider_avail.append(True)

    def revive_provider(self, provider_ind):
        """
        Makes a provider available for sending emails again
        :param provider_ind: Index of the provider
        """
        self.__provider_avail[provider_ind] = True

    def is_available(self, provider_ind):
        return self.__provider_avail[provider_ind]

    def kill_provider(self, provider_ind):
        """
        Makes the provider unavailable for sending attempts
        :param provider_ind: Index of the provider
        """
        self.__provider_avail[provider_ind] = False


def create_message_service():
    """
    Creates a message distribution service and sets the providers available to it
    :return the result message service
    :rtype MessageService
    """
    service = MessageService()
    service.add_provider(MailGunProvider())
    service.add_provider(SendgridProvider())
    return service


message_service = create_message_service()
