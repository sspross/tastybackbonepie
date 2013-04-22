from settings import *


UNIQUE_PREFIX = 'tastybackbonepie'

DEPLOYMENT = {
    'git_repository': 'git@github.com:sspross/%s.git' % UNIQUE_PREFIX,
    'git_branch': 'master',
    'git_remote': 'origin',
    'hosts': ['silvan.spross.ch'],
    'user': 'root',
    'project': 'djangoproject',
    'root': '/root/projects/%s' % UNIQUE_PREFIX,
    'celery_worker': '%s_celery' % UNIQUE_PREFIX,
    'rabbitmq_vhost': UNIQUE_PREFIX,
    'rabbitmq_username': UNIQUE_PREFIX,
    'rabbitmq_password': '',
    'is_stage': False,
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_%s' % UNIQUE_PREFIX,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ADMINS = (
    ('sspross', 'silvan.spross@gmail.com'),
)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'KEY_PREFIX': UNIQUE_PREFIX,
        'VERSION': 1,
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# broker and celery
BROKER_URL = 'amqp://%(rabbitmq_username)s:%(rabbitmq_password)s@localhost:5672/%(rabbitmq_vhost)s' % DEPLOYMENT
CELERY_RESULT_BACKEND = "redis://localhost/0"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYD_CONCURRENCY = 1
CELERY_SEND_EVENTS = False
CELERY_ENABLE_UTC = True

# sentry
RAVEN_CONFIG = {
    'dsn': '',
}
