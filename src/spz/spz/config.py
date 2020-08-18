# -*- coding: utf-8 -*-

"""Configurations for different environments.

    Values can be overridden by specifying 'SPZ_CFG_FILE' environment variable.
"""

from datetime import timedelta

from kombu import Queue


class BaseConfig(object):

    WTF_CSRF_ENABLED = True

    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'

    REMEMBER_COOKIE_DURATION = timedelta(weeks=1)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return '{driver}://{user}:{pw}@{host}/{db}'.format(
                db=self.DB_DB,
                driver=self.DB_DRIVER,
                host=self.DB_HOST,
                pw=self.DB_PW,
                user=self.DB_USER
        )

    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 5}
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    CELERY_BROKER_URL = 'redis://redis:6379'
    CELERY_RESULT_BACKEND = 'redis://redis:6379'
    CELERY_ACCEPT_CONTENT = ['pickle']
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'
    CELERY_DEFAULT_QUEUE = 'default'
    CELERY_QUEUES = (
        Queue('default', routing_key='default'),
        Queue('slow_mails', routing_key='slow_mails')
    )
    CELERY_ROUTES = {
        'spz.tasks.send_slow': {
            'queue': 'slow_mails',
            'routing_key': 'slow_mails'
        },
        'spz.tasks.send_quick': {
            'queue': 'default',
            'routing_key': 'default'
        },
        'spz.tasks.populate': {
            'queue': 'default',
            'routing_key': 'default'
        },
        'spz.tasks.sync_ilias': {
            'queue': 'default',
            'routing_key': 'default'
        },
    }
    CELERY_TIMEZONE = 'UTC'  # like everything else
    CELERYBEAT_SCHEDULE = {
        'populate': {
            'task': 'spz.tasks.populate',
            'schedule': timedelta(minutes=5)
        },
        'sync_ilias': {
            'task': 'spz.tasks.sync_ilias',
            'schedule': timedelta(minutes=15)
        },
    }

    BABEL_DEFAULT_LOCALE = 'de'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Berlin'

    MAIL_SERVER = 'mail'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "spz-signup"
    MAIL_MAX_EMAILS = 10
    MAIL_SUPPRESS_SEND = False
    MAIL_MAX_ATTACHMENT_SIZE = 1024 * 1024 * 8  # 8MB

    CACHE_CONFIG = {'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 30}

    PRIMARY_MAIL = 'no-reply@anmeldung.spz.kit.edu'

    SEMESTER_NAME = 'Testsemester 2020'

    REPLY_TO = [
        'info@spz.kit.edu',
        'englisch@spz.kit.edu',
        'franzoesisch@spz.kit.edu',
        'spanisch@spz.kit.edu',
    ]

    OVERBOOKING_FACTOR = 3

    # The time period the applicants can signoff themselves
    SELF_SIGNOFF_PERIOD = timedelta(days=3)
    # The automatic restock system kicks in;
    # some time later, the RND process is finished and we continue with FCFS (in case there are empty slots)
    RANDOM_WINDOW_CLOSED_FOR = timedelta(hours=36)

    # limit for global amount of attendances; this does not affect attendances for courses that are already
    # done "now"; e.g. intensive
    MAX_ATTENDANCES = 2

    # maximum size, a 'short' waiting list may have
    SHORT_WAITING_LIST = 5

    # maximum amount of vacancies, a course with 'little vacancies' may have
    LITTLE_VACANCIES = 5

    # data for ilias sync
    ILIAS_URL = 'https://scc-ilias-plugins.scc.kit.edu/'
    ILIAS_USERNAME = 'soap_spz'
    ILIAS_PASSWORD = 'mysecretpassword'
    ILIAS_REFID = '123'


class Development(BaseConfig):
    DEBUG = True

    SECRET_KEY = 'dev-secret'
    TOKEN_SECRET_KEY = 'dev-secret'
    ARGON2_SALT = 'dev-secret'

    DB_DB = 'spz'
    DB_DRIVER = 'postgresql'
    DB_HOST = 'postgres'
    DB_USER = 'postgres'
    DB_PW = 'mysecretpassword'


class Testing(BaseConfig):
    TESTING = True

    CACHE_CONFIG = {'CACHE_TYPE': 'null', 'CACHE_NO_NULL_WARNING': True}
    BABEL_DEFAULT_LOCALE = 'en'
    WTF_CSRF_ENABLED = False

    SECRET_KEY = 'test-secret'
    TOKEN_SECRET_KEY = 'test-secret'
    ARGON2_SALT = 'test-secret'

    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'

    DB_DB = 'spz'
    DB_DRIVER = 'postgresql'
    DB_HOST = 'localhost'
    DB_USER = 'postgres'
    DB_PW = ''


class Production(BaseConfig):
    # overwrite in production.cfg

    DB_DB = 'spz'
    DB_DRIVER = 'postgresql'
    DB_HOST = 'localhost'
    DB_USER = 'postgres'
    DB_PW = ''
