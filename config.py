import os


def database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name, 'host': host,
                  'username': username,
                  'password': password})


class Config(object):
    # Statement for enabling the development environment
    DEBUG = False
    TESTING = False

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    DATABASE_CONNECT_OPTIONS = {}

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True


class ProductionDevelopmentConfig(Config):

    #Define database connection parameters
    __host = os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST', 'localhost')
    __username = os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME', 'cituser')
    __password = os.getenv('OPENSHIFT_POSTGRESQL_DB_PASSWORD', 'citpasswd')
    __db_name = os.getenv('OPENSHIFT_APP_NAME', 'cit')

    # Define production database
    SQLALCHEMY_DATABASE_URI = \
        database_uri(__host, __username, __password, __db_name)

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.getenv('OPENSHIFT_CSRF_SESSION_KEY', None)

    # Secret key for signing cookies
    SECRET_KEY = os.getenv('OPENSHIFT_SECRET_KEY', 'jd&%G#43WG~dn6')

    SITE_TITLE = os.getenv('OPENSHIFT_SITE_TITLE', 'Hi, Developer :)')

    # Facebook settings
    CONSUMER_KEY = os.getenv('OPENSHIFT_CONSUMER_KEY', '597071850435446')
    CONSUMER_SECRET = os.getenv('OPENSHIFT_CONSUMER_SECRET',
                                'c0e023b09461c502cd3cd7121d205735')

    if 'OPENSHIFT_POSTGRESQL_DB_HOST' not in os.environ.keys():

        # Statement for enabling the development environment
        DEBUG = True

        # Enable protection against *Cross-site Request Forgery (CSRF)*
        CSRF_ENABLED = False


class TestingConfig(Config):
    # Statement for enabling the development environment
    DEBUG = True
    TESTING = True

    # Disable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = False

    #Define database connection parameters
    __host = 'localhost'
    __username = 'cituser'
    __password = 'citpasswd'
    __db_name = 'cit_test'

    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = \
        database_uri(__host, __username, __password, __db_name)

    # Secret key for signing cookies
    SECRET_KEY = "jd&%G#43WG~dn6"

    SITE_TITLE = "TEST"

    # Facebook settings
    CONSUMER_KEY = '597071850435446'
    CONSUMER_SECRET = 'c0e023b09461c502cd3cd7121d205735'
