from celery_task import add, import_file_task
import unittest
from config import Config
from app import create_app
from database import db_session, init_db

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProdcutModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        init_db()

    def tearDown(self):
        db_session.rollback()
        db_session.flush()
        db_session.remove()
        self.app_context.pop()

    def test_add(self):
        self.assertEqual(add.delay(1, 2).get(), 3)

    def test_add_fail(self):
        self.assertEqual(add.delay(1, 2).get(), 5)

    def test_import_file_task(self):
        self.assertEqual(import_file_task.delay("test.csv").get(), 3)

if __name__ == '__main__':
    unittest.main(verbosity=2)