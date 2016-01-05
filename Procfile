web: gunicorn RobustMail:app --log-file -
worker: celery worker --app=core.services.message_service.celery --without-gossip --without-mingle --without-heartbeat
