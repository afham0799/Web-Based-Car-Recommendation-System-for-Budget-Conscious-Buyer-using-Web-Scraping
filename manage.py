# manage.py

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# Initialize Flask-Script
manager = Manager(app)
migrate = Migrate(app, db)

# Add Flask-Migrate commands
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
