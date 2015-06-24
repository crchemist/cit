from cit import create_app
from cit.db import db
from unittest import TestCase as Base
import init_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database
from sqlalchemy import create_engine
from config import database_uri, Config, TestingConfig
import sqlalchemy.exc as sqlalchemy_exc
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT,\
    ISOLATION_LEVEL_READ_COMMITTED
from cit import Comment
import json

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

        try:
            session.connection().connection.\
                set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            session.execute('DROP DATABASE ' + TestingConfig.db_name)
            session.connection().connection.\
                set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
        except sqlalchemy_exc.DBAPIError:
            print('Testing DB "cit_test" is absent. New DB "cit_test" \
will be created')
        finally:
            session.commit()
            session.rollback()
            session.close_all()
            engine.dispose()

        session.connection().connection.\
            set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        session.execute('CREATE DATABASE ' + TestingConfig.db_name)
        session.connection().connection.\
            set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)

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

    def test_adding_comments_logged_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            comment = dict(issue_id=1, msg='test test')
            response = self.client.post('/comments/', data=comment)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        response_in_json = json.loads(response.data)
        comment_id = response_in_json['id']
        comment_from_db = Comment.query.filter_by(id=comment_id).first()

        assert response.status_code == 201

        assert (str(comment['issue_id']) == comment_from_db.issue_id) and\
               (comment['msg'] == comment_from_db.message)

if __name__ == "__main__":
    import unittest

    unittest.main()
