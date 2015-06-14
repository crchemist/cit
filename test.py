from cit import create_app
from cit.db import db
from unittest import TestCase as Base
import init_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database
from sqlalchemy import create_engine
from config import database_uri, Config

engine = create_engine(database_uri(Config.host, Config.username,
                                    Config.password, 'postgres'))


class TestCase(Base):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config.TestingConfig')
        cls.client = cls.app.test_client()
        cls._ctx = cls.app.test_request_context()
        cls._ctx.push()

        session = sessionmaker(bind=engine)()

        session.connection().connection.set_isolation_level(0)
        session.execute('CREATE DATABASE cit_test')
        session.connection().connection.set_isolation_level(1)

        db.engine.execute('CREATE EXTENSION postgis;')
        db.engine.execute('CREATE EXTENSION plv8;')

        db.create_all()
        init_db.InitDB(cls.app).generate_test_data()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        drop_database(db.engine.url)
        db.get_engine(cls.app).dispose()

    def setUp(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self._ctx.pop()

class TestModel(TestCase):

    def test_adding_comments_unlogged_user(self):
        comment = dict(issue_id=1, msg='test test')

        response = self.client.post('/comments/', data=comment)

        assert response.status_code == 401

if __name__ == "__main__":
    import unittest

    unittest.main()
