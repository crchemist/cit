# cit
Installation

  * `virtualenv env`
  * `source env/bin/activate`
  *  Install posgresql-9.4, postgis, plv8 and postgresql-dev* packages.
  * `pip install -r requirements.txt`
  * Create `cituser:citpasswd@cit` database.
  * Create plv8 extension in psql: `create extension plv8;`
  * Create postgis extension in psql: `CREATE EXTENSION postgis;`
  * `alembic upgrade head`
  * `python init_db.py`
