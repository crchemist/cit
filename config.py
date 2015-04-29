# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

#Define database connection
host = os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST', localhost)
port = ('OPENSHIFT_POSTGRESQL_DB_PORT', 5432) 
username = os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME', cituser)
password = os.getenv('OPENSHIFT_POSTGRESQL_DB_PASSWORD', citpasswd)
db_name = os.getenv('OPENSHIFT_APP_NAME', cit) 

# Define the database - we are working with 
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. format(**{"db_name":db_name, "host":host, "username":username, "password":password })
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
