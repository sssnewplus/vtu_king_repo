from flask_migrate import Migrate, upgrade
from app import create_app, db

def run_migrations():
    # Automates the database migration process programmatically.
    app = create_app()
    # Initialize Flask-Migrate with app and db
    Migrate(app, db)

    with app.app_context():
        # Upgrade the database to the latest migration
        upgrade()
        print("Database has been successfully upgraded to the latest migration.")
