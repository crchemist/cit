from cit import create_app
from cit.db import db
from unittest import TestCase as Base
import init_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database, database_exists
from sqlalchemy import create_engine
from config import database_uri, Config, TestingConfig
import sqlalchemy.exc as sqlalchemy_exc
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT,\
    ISOLATION_LEVEL_READ_COMMITTED
from cit import Comment
import json
from cit.auth.models import User, organization_relationships
from cit.organizations.models import Organization

engine = create_engine(database_uri(Config.host, Config.username,
                                    Config.password, 'postgres'))


class TestCase(Base):
    app = None

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
            print('Old testing DB "cit_test" has been dropped')
        except sqlalchemy_exc.DBAPIError:
            message = 'Testing DB "cit_test" is absent. New DB "cit_test" ' \
                      'will be created'
            print(message)

        session.connection().connection.\
            set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        session.execute('CREATE DATABASE ' + TestingConfig.db_name)
        session.connection().connection.\
            set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
        print('New testing DB "cit_test" has been created')

        db.engine.execute('CREATE EXTENSION postgis;')
        db.engine.execute('CREATE EXTENSION plv8;')

        db.create_all()
        init_db.InitDB(cls.app).generate_test_data()
        user = User.query.filter_by(id=1).first()
        init_db.InitDB(cls.app).make_user_as_admin(user.fb_id)
        init_db.InitDB(cls.app).generate_test_data()
        pass

    @classmethod
    def tearDownClass(cls):
        db.session.close()
        db.session.remove()
        drop_database(db.engine.url)
        db.get_engine(cls.app).dispose()
        message = 'All tests has been run. ' \
                  'Testing DB "cit_test" has been dropped.'
        print(message)

    def setUp(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self._ctx.pop()


class TestModel(TestCase):

    def test_add_comment_unauth_user(self):
        comment = dict(issue_id=1, msg='test test')

        response = self.client.post('/comments/', data=comment)

        message_init = 'A problem with adding comment by unauthorised user.\n'

        message = message_init + \
            "response.status_code isn't equal to 401."
        TestCase.assertEqual(self, response.status_code, 401, msg=message)

        message = message_init + \
            "response.data doesn't contain message 'Permission denied'."
        TestCase.assertIn(self, 'Permission denied',
                          response.data, msg=message)

    def test_add_comment_auth_user(self):
        user_id = 2  # this user doesn't have superuser rights
        issue_id = 1
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            comment = dict(issue_id=issue_id, msg='test test')
            response = c.post('/comments/', data=comment)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        response_in_json = json.loads(response.data)
        comment_id = response_in_json['id']
        comment_from_db = Comment.query.filter_by(id=comment_id).first()

        message = 'A problem with adding comment by authorised user.\n' \
                  "response.status_code isn't equal to 201."
        TestCase.assertEqual(self, response.status_code, 201, msg=message)

        message = 'A problem with adding comment by authorised user to DB.'
        expr = (str(comment['issue_id']) == comment_from_db.issue_id) and\
               (comment['msg'] == comment_from_db.message)
        TestCase.assertTrue(self, expr, msg=message)

    def test_del_comment_unauth_user(self):
        comment_id = 2
        response = self.client.delete('/comments/%d/' % comment_id)

        message_init = 'A problem with deleting comment by' + \
            'unauthorised user.\n'

        message = message_init + \
            "response.status_code isn't equal to 401."
        TestCase.assertEqual(self, response.status_code, 401, msg=message)

        message = message_init + \
            "response.data doesn't contain message 'Permission denied'."
        TestCase.assertIn(self, 'Permission denied',
                          response.data, msg=message)

    def test_del_comment_auth_user_1(self):
        # the func tests comment deleting by a user who didn't create
        # this comment
        user_id = 2
        comment_id = 1
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.delete('/comments/%d/' % comment_id)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        comment_from_db = Comment.query.filter_by(id=comment_id).first()

        message = 'Test a status of comment deleting by a user who has no ' + \
                  'permission for this operation.\n' + \
                  "response.status_code isn't equal to 403."
        TestCase.assertEqual(self, response.status_code, 403, msg=message)

        message = 'A comment was successfully deleted by unauthorised user.'
        TestCase.assertIsNotNone(self, comment_from_db, msg=message)

    def test_del_comment_auth_user_2(self):
        user_id = 2
        comment_id = 2
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.delete('/comments/%d/' % comment_id)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        comment_from_db = Comment.query.filter_by(id=comment_id).first()

        message = 'A status of comment deleting by comment author\n' + \
                  "isn't equal to 204."
        TestCase.assertEqual(self, response.status_code, 204, msg=message)

        message = 'A comment was successfully deleted by authorised user.'
        TestCase.assertIsNone(self, comment_from_db, msg=message)

    def test_del_comment_auth_user_3(self):
        # a test for superuser privilege to delete user comments.
        user_id = 1  # this user has the superuser rights
        comment_id = 2
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.delete('/comments/%d/' % comment_id)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        comment_from_db = Comment.query.filter_by(id=comment_id).first()

        message = 'A status of comment deleting by superuser\n' + \
                  "isn't equal to 204."
        TestCase.assertEqual(self, response.status_code, 204, msg=message)

        message = 'A comment was successfully deleted by superuser.'
        TestCase.assertIsNone(self, comment_from_db, msg=message)

    def test_del_notexist_comment(self):
        user_id = 2
        comment_id = 3  # the comment with id = 3 doesn't exist
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.delete('/comments/%d/' % comment_id)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        message = 'A status of deleting nonexistent comment' + \
            "isn't equal to 404."
        TestCase.assertEqual(self, response.status_code, 404, msg=message)

    def test_adding_organization_unauth_user(self):
        organization = dict(name='Test Organization',
                            address='POINT(49.836134 24.023151)')
        response = self.client.post('/organizations/', data=organization)

        message_init = "A user isn't authorised.\n" + \
            'A problem with test connected to organization adding by ' + \
            'nonsuperuser.\n'

        message = message_init + "response.status_code isn't equal to 401."
        TestCase.assertEqual(self, response.status_code, 401, msg=message)

        message = message_init + \
            "response.data doesn't contain message " + \
            "'Admin permissions required'."
        TestCase.assertIn(self, 'Admin permissions required',
                          response.data, msg=message)

    def test_adding_organization_nonsuperuser(self):
        user_id = 2  # this user doesn't have superuser rights
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            organization = dict(name='Test Organization',
                                address='POINT(49.836134 24.023151)')
            response = \
                self.client.post('/organizations/',
                                 data=json.dumps(organization),
                                 content_type='application/json')
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        message_init = "A user is authorised but isn't a superuser.\n" + \
            'A problem with test connected to organization adding by ' + \
            'nonsuperuser.\n'

        message = message_init + \
            "response.status_code isn't equal to 401."
        TestCase.assertEqual(self, response.status_code, 401, msg=message)

        message = message_init + \
            "response.data doesn't contain message " + \
            "'Admin permissions required'."
        TestCase.assertIn(self, 'Admin permissions required',
                          response.data, msg=message)

    def test_adding_organization_superuser(self):
        user_id = 1  # this user has the superuser rights
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            organization = dict(name='Test Organization',
                                address='POINT(49.836134 24.023151)')
            response = \
                self.client.post('/organizations/',
                                 data=json.dumps(organization),
                                 content_type='application/json')
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        response_in_json = json.loads(response.data)
        organization_id = response_in_json['id']
        org_from_db = Organization.query.filter_by(id=organization_id).first()

        message = 'A user has the superuser rights.\n' + \
                  'A problem with test concerned to organization ' + \
                  'adding by a superuser.\n' + \
                  "response.status_code isn't equal to 201."
        TestCase.assertEqual(self, response.status_code, 201, msg=message)

        message = 'A problem with adding organization by a superuser to DB.'
        expr = (str(organization['name']) == org_from_db.name) and\
               (organization['address'] == org_from_db.address)
        TestCase.assertTrue(self, expr, msg=message)

    def test_adding_user_organization_rel_unauth_user(self):
        org_id = 1
        response = self.client.post('/organizations/%d/add-user/' % org_id)

        message_init = 'A problem with adding user to user-organization ' + \
            'relationship by unauthorised user.\n'

        message = message_init + \
            "response.status_code isn't equal to 401."
        TestCase.assertEqual(self, response.status_code, 401, msg=message)

        message = message_init + \
            "response.data doesn't contain message 'Permission denied'."
        TestCase.assertIn(self, 'Permission denied',
                          response.data, msg=message)

    def test_adding_user_organization_rel_auth_user_1(self):
        user_id = 2
        org_id = 1
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.post('/organizations/%d/add-user/' % org_id)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        response_in_json = json.loads(response.data)
        message_init = 'A problem with adding user to user-organization ' + \
            'relationship by authorised user.\n'

        message = message_init + \
            "response.data doesn't contain substring 'was established'"
        TestCase.assertIn(self, 'was established', response.data, msg=message)

        message = message_init + \
            "response_in_json['user_id'] != user_id"
        TestCase.assertEqual(self, response_in_json['user_id'],
                             user_id, msg=message)

        message = message_init + \
            "response_in_json['org_id'] != org_id"
        TestCase.assertEqual(self, response_in_json['org_id'],
                             org_id, msg=message)

        message = message_init + \
            "'organization_relationships' table doesn't contain the raw" + \
            ' (%d, %d)' % (user_id, org_id)
        x = db.session.query(organization_relationships).\
            filter(organization_relationships.c.organization_id == org_id).\
            filter(organization_relationships.c.user_id == user_id).all()
        TestCase.assertEqual(self, x, [(user_id, org_id)], msg=message)

        message = message_init + \
            "response.status_code isn't equal to 201."
        TestCase.assertEqual(self, response.status_code, 201, msg=message)

    def test_adding_user_organization_rel_auth_user_2(self):
        user_id = 2
        org_id = 2
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.post('/organizations/%d/add-user/' % org_id)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        message_init = 'A problem with creation user-organization' + \
            'relationship that already exists.\n'

        message = message_init + \
            "response.data doesn't contain substring 'IntegrityError'"
        TestCase.assertIn(self, 'IntegrityError',
                          response.data, msg=message)

        message = message_init + \
            "response.status_code isn't equal to 409."
        TestCase.assertEqual(self, response.status_code, 409, msg=message)

    def test_adding_user_organization_rel_auth_user_3(self):
        user_id = 1
        org_id = 3  # such organization doesn't exist
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.post('/organizations/%d/add-user/' % org_id)
            with c.session_transaction() as sess:
                sess.pop('user_id', None)

        message_init = 'A problem with creation user-organization' + \
            "relationship where the organization doesn't exist.\n"

        message = message_init + \
            "response.data doesn't contain substring 'FlushError'"
        TestCase.assertIn(self, 'FlushError',
                          response.data, msg=message)

        message = message_init + \
            "response.status_code isn't equal to 404."
        TestCase.assertEqual(self, response.status_code, 404, msg=message)

if __name__ == "__main__":
    import unittest

    unittest.main()
