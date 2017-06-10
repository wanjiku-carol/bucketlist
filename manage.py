import os
import unittest
# class for handling a set of commands
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app

app = create_app(config_name=os.getenv('APP_SETTINGS'))
# initialize the app with all its configurations
migrate = Migrate(app, db)
# create an instance of class that will handle our commands
manager = Manager(app)
# Define the migration command to always be preceded by the word "db" as in
# running migrations command
manager.add_command('db', MigrateCommand)

# define our command for testing called "test" which will be applied in
# python manage.py test


@manager.command
def test():
    """runs unittests without test coverage"""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
