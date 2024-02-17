from project import create_app, db, models

# Create the Flask application instance
app = create_app()

# Create the database tables within the application context
with app.app_context():
    db.create_all()
