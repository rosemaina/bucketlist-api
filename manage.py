# manage.py
import unittest
import os

from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app
from app import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """This automates tests by running tests"""
    # gets test location and pattern
    tests = unittest.TestLoader().discover('./tests', 'test*.py')
    #runs the tests found
    results = unittest.TextTestRunner(verbosity=2).run(tests)
    if results.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
