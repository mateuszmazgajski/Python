# app/routes.py
from app import app, db  # Ensure this import is correct
from flask import render_template, redirect, url_for, flash, abort
from flask import redirect, url_for
from flask import jsonify, request
from app.forms import calculate_available_hours
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, Booking, Therapist
from app.forms import LoginForm, BookingForm, RegistrationForm, AppointmentForm
from datetime import datetime, date, time

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/book_office', methods=['GET', 'POST'])
@login_required
def book_office():
    form = BookingForm()
    if form.validate_on_submit():
        #selected_office = form.office.data
        selected_office = request.form.get('selected_office')
        selected_date = form.date.data
        selected_time = form.start_time.data

        start_time_obj = datetime.strptime(selected_time, '%H:%M').time()
        booking = Booking(office=selected_office, date=form.date.data, start_time=start_time_obj, user=current_user, timestamp=datetime.now()) # start_time=form.start_time.data
        
        db.session.add(booking)
        db.session.commit()
        flash('Booking successful!', 'success')
        #return redirect(url_for('book_office'))
    else:
        print(form.errors.items())
        print('Selected office:', request.form.get('selected_office'))
        print('Selected date:', request.form.get('selected_time'))
        print('Selected time:', form.start_time.data)
    return render_template('book_office.html', form=form)

@app.route('/all_bookings')
@login_required
def all_bookings():
    # Check if the current user has the "admin" role
    if current_user.username != 'admin':
        abort(403)  # HTTP 403 Forbidden
    bookings = Booking.get_all_bookings()
    return render_template('all_bookings.html', bookings=bookings)

@app.route('/my_bookings')
@login_required
def my_bookings():
    # Adding current_date and current_time to the template context
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    bookings = Booking.query.filter_by(user=current_user).all()
    return render_template('my_bookings.html', bookings=bookings, current_date=current_date, current_time=current_time)

@app.route('/remove_booking/<int:booking_id>', methods=['POST'])
@login_required
def remove_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if the logged-in user is the owner of the booking
    if current_user.id == booking.user_id:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking removed successfully!', 'success')
    else:
        flash('You are not authorized to remove this booking.', 'danger')

    return redirect(url_for('all_bookings'))

@app.route('/remove_my_booking/<int:booking_id>', methods=['POST', 'DELETE'])
@login_required
def remove_my_booking(booking_id):
    if request.method in ['POST', 'DELETE']:
        booking = Booking.query.get(booking_id)
        if booking and booking.user == current_user:
            db.session.delete(booking)
            db.session.commit()
            flash('Booking removed successfully!', 'success')
        else:
            flash('Booking not found or unauthorized!', 'danger')
    return redirect(url_for('my_bookings'))

@app.route('/get_available_hours', methods=['GET'])
def get_available_hours():
    selected_office = request.args.get('office')
    selected_date = request.args.get('date')
    # Call your existing function to get available hours
    available_hours = calculate_available_hours(selected_office, selected_date)

    # Return the available hours as JSON
    return jsonify({'available_hours': available_hours})

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():

    # Create the appointment form
    form = AppointmentForm()
    if form.validate_on_submit():
        # Process the form data and book the appointment
        # Implement your logic here
        
        # Redirect to a success page or render a success message
        pass
        flash('Booking successful!', 'success')

    return render_template('book_appointment.html', form=form)
