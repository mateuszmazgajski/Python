# app/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    #role = db.Column(db.String(20))  # New field for role
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Therapist model
class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    # Add other fields as needed, such as availability

    def __repr__(self):
        return f"Therapist('{self.name}', '{self.specialty}')"
    
# Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    therapist = db.relationship('Therapist', backref=db.backref('appointments', lazy=True))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    # Add other fields as needed, such as user_id for the person booking the appointment

    def __repr__(self):
        return f"Appointment('{self.therapist}', '{self.date}', '{self.time}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    @staticmethod
    def get_all_bookings():
        return Booking.query.all()
    def __repr__(self):
        return f"Booking('{self.office}','{self.date}', '{self.start_time}', '{self.timestamp}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
