from datetime import datetime, timedelta
import unittest
from app import create_app, db
from config import TestConfig
from app.models import User

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app = create_app(TestConfig)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()        

if __name__ == '__main__':
    unittest.main(verbosity=2)