# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
#identify variable db_name and user pass

db_username = os.getenv("READER_USERNAME")
db_password = os.getenv("READER_PASSWORD")
db_name = os.getenv("DATABASE_NAME") or 'cit'

# Define the database - we are working with
# SQLite change for postpreSQL
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://localhost/cit', isolation_level="AUTOCOMMIT")
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
