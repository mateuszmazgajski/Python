# run.py
from app import app, db
from app.models import User

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        # Check if the test user already exists
        test_user = User.query.filter_by(username='testuser').first()
        admin_user = User.query.filter_by(username='admin').first()

        # Update the existing test user if it exists
        if test_user:
            test_user.set_password('newpassword')
            db.session.commit()
        else:
            # Create the test user if it doesn't exist
            test_user = User(username='testuser')
            test_user.set_password('testpassword')
            db.session.add(test_user)
            db.session.commit()

        # Update the existing admin user if it exists
        if admin_user:
            admin_user.set_password('admin')
            db.session.commit()
        else:
            # Create the admin user if it doesn't exist
            admin_user = User(username='admin')
            admin_user.set_password('admin')
            db.session.add(admin_user)
            db.session.commit()

    # Run the Flask application
    app.run(debug=True)
