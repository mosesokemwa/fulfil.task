import io
from tasks.celery_task import add, import_file_task
import unittest
from config.settings import Config
from app import create_app
from models import db_session, init_db
from flask import url_for

from models.models import Product


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class CeleryTaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)  # type: ignore
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


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)  # type: ignore
        self.app_context = self.app.app_context()
        self.app_context.push()
        init_db()

    def tearDown(self):
        db_session.rollback()
        db_session.flush()
        db_session.remove()
        self.app_context.pop()

    def test_upload_csv(self):
        """Test can upload csv file."""
        # data = {'name': 'this is a name', 'age': 12}
        # data = {key: str(value) for key, value in data.items()}
        # data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')
        data = {"file": (io.BytesIO(b"abcdef"), "test.csv")}
        # self.login()
        response = self.client.post(  # type: ignore
            url_for("adverts.save"),
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        self.assertIn(b"Your item has been saved.", response.data)
        advert = Product.query.get(1)
        self.assertIsNotNone(advert.logo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
