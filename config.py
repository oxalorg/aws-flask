import os
_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    ADMINS = frozenset(['mitesh@oxal.org'])
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                'This string will be replaced with a proper key in production.')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
    DATABASE_CONNECT_OPTIONS = {}

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' \
                                + os.environ['DB_USERNAME'] + ':' + os.environ['DB_PASSWORD'] \
                                +'@' + os.environ['DB_HOSTNAME']  +  ':' + os.environ['DB_PORT'] \
                                + '/' + os.environ['DB_NAME']


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    CELERY_CONFIG = {'CELERY_ALWAYS_EAGER': True}
    SOCKETIO_MESSAGE_QUEUE = None


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
