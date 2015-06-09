import os


def database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name, 'host': host,
                  'username': username,
                  'password': password})


class Config(object):
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

    # From the one hand documentation
    # "https://pythonhosted.org/Flask-Testing/#testing-with-sqlalchemy"
    # says
    # "Another gotcha is that Flask-SQLAlchemy also removes the session
    # instance at the end of every request (as should any thread safe
    # application using SQLAlchemy with scoped_session). "
    #
    # On the other hand the default value of SQLALCHEMY_COMMIT_ON_TEARDOWN
    # is False.
    # See  https://github.com/mitsuhiko/flask-sqlalchemy/blob/master/flask_sqlalchemy/__init__.py#L791
    # or https://github.com/danjac/Flask-Testing/blob/master/docs/index.rst
    # Explicit setting this configuration key to True is made for reliability.
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    DATABASE_CONNECT_OPTIONS = {}

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

try:
    class ProductionConfig(Config):

        #Define database connection parameters
        __host = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
        __username = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
        __password = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
        __db_name = os.environ['OPENSHIFT_APP_NAME']

        # Define production database
        SQLALCHEMY_DATABASE_URI = \
            database_uri(__host, __username, __password, __db_name)

        # Use a secure, unique and absolutely secret key for
        # signing the data.
        # for details see http://flask.pocoo.org/snippets/3/
        # and http://en.wikipedia.org/wiki/CSRF
        CSRF_SESSION_KEY = os.environ['OPENSHIFT_CSRF_SESSION_KEY']

        # Secret key for signing cookies
        SECRET_KEY = os.environ['OPENSHIFT_SECRET_KEY']

        SITE_TITLE = os.environ['OPENSHIFT_SITE_TITLE']

        # Facebook settings
        CONSUMER_KEY = os.environ['OPENSHIFT_CONSUMER_KEY']
        CONSUMER_SECRET = os.environ['OPENSHIFT_CONSUMER_SECRET']
except KeyError:
    print('You are not in Production mode')
    # For entering production mode please comment the string
    # app.config.from_object('config.DevelopmentConfig')
    # and uncomment the string
    # app.config.from_object('config.ProductionConfig')
    # in cit/__init__.py


class DevelopmentConfig(Config):
    # Statement for enabling the development environment
    DEBUG = True

    # Disable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = False

    # Define database connection parameters
    __host = 'localhost'
    __username = 'cituser'
    __password = 'citpasswd'
    __db_name = 'cit'

    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = \
        database_uri(__host, __username, __password, __db_name)

    # Secret key for signing cookies
    SECRET_KEY = "5e3r1t"

    SITE_TITLE = "Hi:)"

    # Facebook settings
    CONSUMER_KEY = '597071850435446'
    CONSUMER_SECRET = 'c0e023b09461c502cd3cd7121d205735'


class TestingConfig(DevelopmentConfig):
    TESTING = True

    #Define database connection parameters
    __host = 'localhost'
    __username = 'cituser'
    __password = 'citpasswd'
    __db_name = 'cit_test'

    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = \
        database_uri(__host, __username, __password, __db_name)
