web: gunicorn RobustMail:app --log-file -
worker: celery worker --app=core.services.message_service.celery
