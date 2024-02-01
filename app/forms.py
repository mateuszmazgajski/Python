# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import DateField, DateField, TimeField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length
from wtforms.widgets import Input, DateInput, TimeInput
from datetime import date, datetime
from app.models import Booking

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class BookingForm(FlaskForm):
    hour_choices = [
        (f'{hour:02d}:00', f'{hour:02d}:00') for hour in range(8, 22)
    ]
    office_choices = ['Office 1', 'Office 2', 'Office 3', 'Office 4']
    office = SelectField('Select an office', choices=office_choices, validators=[DataRequired()],default=office_choices[0], coerce=str)
    date = DateField('Date', validators=[DataRequired()], default=date.today(), render_kw={'min': date.today()})
    start_time = SelectField('Select hour', choices=hour_choices, validators=[DataRequired()], coerce=str)
    submit = SubmitField('Book Office')

    def populate_hour_choices(self):
        # Your implementation of get_available_hours
        selected_office = self.office.data
        selected_date = self.date.data
        available_hours = calculate_available_hours(selected_office, selected_date)  # Adjust this to get available hours for the current date
        #print("Available Hours:", available_hours)

        # Set choices for the start_time field
        self.start_time.choices = available_hours

def calculate_available_hours(selected_office, selected_date):

    # Calculate the current date
    now = date.today()
    current_date = now.strftime('%Y-%m-%d')
    # Check if the selected date is the current date
    if selected_date == current_date:
        # If the selected date is the current date, get the current time
        current_time = datetime.now().time()
        start_hour = int(current_time.strftime('%H')) + 1
        # Use the current time to filter available hours
        available_hours = [
            (f'{hour:02d}:00', f'{hour:02d}:00') for hour in range(start_hour, 22)
        ]
        print(available_hours)
    else:
        # If the selected date is in the future, all hours are available
        available_hours = [
            (f'{hour:02d}:00', f'{hour:02d}:00') for hour in range(8, 22)
        ]

    # Query your database to get booked hours
    booked_hours = set()
    booked_records = Booking.query.filter_by(office=selected_office, date=selected_date).all()

    # Loop through booked records and extract the hours
    for record in booked_records:
        booked_hours.add(record.start_time.hour)

    # Remove booked hours from available hours
    for hour in booked_hours:
        available_hours.remove((f'{hour:02d}:00', f'{hour:02d}:00'))

    return available_hours




