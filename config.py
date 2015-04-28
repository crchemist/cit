# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

#Database connection parameters
db_host = db_name = os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST','127.0.0.1')
db_port = db_name = ('OPENSHIFT_POSTGRESQL_DB_PORT','5432')
db_username = db_name = os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME','User')
db_password = db_name = os.getenv('OPENSHIFT_POSTGRESQL_DB_PASSWORD','qwer')
db_name = os.getenv("DATABASE_NAME",'citDb')

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://User:qwer@localhost/citDb'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
# CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "SEcr$t"

# Secret key for signing cookies
SECRET_KEY = "5e3r1t"
SITE_TITLE="Hi:)"

# Facebook settings
CONSUMER_KEY = '597071850435446'
CONSUMER_SECRET = 'c0e023b09461c502cd3cd7121d205735'
