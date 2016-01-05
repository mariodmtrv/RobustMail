import os

SETTINGS = {"MAILGUN_APIKEY": os.getenv("MAILGUN_API_KEY"),
            "MAILGUN_BASE_URL": os.getenv("MAILGUN_DOMAIN"),
            "MESSAGE_BROKER_URL": os.getenv("CLOUDAMQP_URL"),
            "SENDGRID_USERNAME": os.getenv("SENDGRID_USERNAME"),
            "SENDGRID_PASSWORD": os.getenv("SENDGRID_PASSWORD"),
            "REDIS_URL": os.getenv("REDISCLOUD_URL")
            }
