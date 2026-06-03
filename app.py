from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from functools import wraps
import json
import os
import pymysql

# Install as MySQLdb for compatibility
pymysql.install_as_MySQLdb()

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ensure secret key is set
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = os.urandom(24)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Database Models (same as before)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('hospital_admin', 'blood_donor', 'blood_bank_manager'), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Donor(db.Model):
    __tablename__ = 'donors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=False)
    age = db.Column(db.Integer)
    weight = db.Column(db.Numeric(5,2))
    medical_conditions = db.Column(db.Text)
    eligibility_status = db.Column(db.Boolean, default=True)
    last_donation_date = db.Column(db.Date)
    total_donations = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref=db.backref('donor_profile', uselist=False))

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), unique=True, nullable=False)
    quantity_units = db.Column(db.Integer, default=0)
    critical_threshold = db.Column(db.Integer, default=10)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class EmergencyRequest(db.Model):
    __tablename__ = 'emergency_requests'
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Enum('low', 'medium', 'high', 'critical'), default='medium')
    patient_name = db.Column(db.String(100))
    patient_age = db.Column(db.Integer)
    patient_condition = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'fulfilled', 'cancelled'), default='pending')
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    fulfillment_date = db.Column(db.DateTime)
    hospital = db.relationship('User', backref=db.backref('emergency_requests', lazy=True))

class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    donation_time = db.Column(db.Time)
    status = db.Column(db.Enum('scheduled', 'completed', 'cancelled'), default='scheduled')
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=False)
    quantity_units = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    donor = db.relationship('User', backref=db.backref('donations', lazy=True))

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Role decorators
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please login to access this page.', 'warning')
                return redirect(url_for('login'))
            if current_user.role not in roles:
                flash('Access denied. Insufficient permissions.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Test database connection route
@app.route('/test_db')
def test_db():
    try:
        # Try to query the database
        result = db.session.execute('SELECT 1').scalar()
        return jsonify({'status': 'success', 'message': 'Database connection working!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# All other routes remain the same as in previous code
# (Include all the route functions from earlier)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, role=role, full_name=full_name, phone=phone, address=address)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        if role == 'blood_donor':
            blood_type = request.form.get('blood_type')
            if blood_type:
                donor = Donor(user_id=user.id, blood_type=blood_type)
                db.session.add(donor)
                db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    inventory = Inventory.query.all()
    inventory_data = [
        {'blood_type': inv.blood_type, 'quantity': inv.quantity_units, 
         'critical': inv.quantity_units < inv.critical_threshold}
        for inv in inventory
    ]
    
    if current_user.role == 'hospital_admin':
        emergency_requests = EmergencyRequest.query.filter_by(hospital_id=current_user.id).order_by(
            EmergencyRequest.request_date.desc()).all()
    else:
        emergency_requests = EmergencyRequest.query.filter_by(status='pending').order_by(
            db.case((EmergencyRequest.priority == 'critical', 1),
                   (EmergencyRequest.priority == 'high', 2),
                   (EmergencyRequest.priority == 'medium', 3),
                   (EmergencyRequest.priority == 'low', 4)),
            EmergencyRequest.request_date.asc()).all()
    
    thirty_days_ago = datetime.now() - timedelta(days=30)
    donations = Donation.query.filter(
        Donation.scheduled_date >= thirty_days_ago.date(),
        Donation.status == 'completed'
    ).all()
    
    upcoming_donations = []
    if current_user.role == 'blood_donor':
        upcoming_donations = Donation.query.filter_by(
            donor_id=current_user.id, 
            status='scheduled'
        ).filter(Donation.scheduled_date >= datetime.now().date()).order_by(Donation.scheduled_date).all()
    
    shortages = [inv for inv in inventory if inv.quantity_units < inv.critical_threshold]
    if shortages and current_user.role == 'blood_bank_manager':
        shortage_msg = f"⚠️ Critical shortage detected for: {', '.join([s.blood_type for s in shortages])}"
        flash(shortage_msg, 'warning')
    
    total_units = sum(inv.quantity_units for inv in inventory)
    total_donors = Donor.query.count()
    pending_requests = EmergencyRequest.query.filter_by(status='pending').count()
    
    return render_template('dashboard.html', 
                         inventory=inventory_data,
                         emergency_requests=emergency_requests,
                         donations=donations,
                         upcoming_donations=upcoming_donations,
                         total_units=total_units,
                         total_donors=total_donors,
                         pending_requests=pending_requests,
                         shortages_count=len(shortages),
                         user_role=current_user.role)

@app.route('/api/inventory')
@login_required
def api_inventory():
    inventory = Inventory.query.all()
    return jsonify([{
        'blood_type': inv.blood_type,
        'quantity': inv.quantity_units,
        'critical_threshold': inv.critical_threshold
    } for inv in inventory])

@app.route('/api/donation_trends')
@login_required
def api_donation_trends():
    last_30_days = datetime.now() - timedelta(days=30)
    donations = Donation.query.filter(
        Donation.scheduled_date >= last_30_days.date(),
        Donation.status == 'completed'
    ).all()
    
    trends = {}
    for donation in donations:
        date_str = donation.scheduled_date.strftime('%Y-%m-%d')
        if date_str not in trends:
            trends[date_str] = 0
        trends[date_str] += donation.quantity_units
    
    all_dates = [(last_30_days + timedelta(days=i)).date().strftime('%Y-%m-%d') 
                 for i in range(31)]
    result_counts = [trends.get(date, 0) for date in all_dates]
    
    return jsonify({'dates': all_dates, 'counts': result_counts})

@app.route('/emergency_requests', methods=['GET', 'POST'])
@login_required
@role_required('hospital_admin')
def emergency_requests():
    if request.method == 'POST':
        emergency = EmergencyRequest(
            hospital_id=current_user.id,
            blood_type=request.form.get('blood_type'),
            quantity=int(request.form.get('quantity')),
            priority=request.form.get('priority'),
            patient_name=request.form.get('patient_name'),
            patient_age=int(request.form.get('patient_age')) if request.form.get('patient_age') else None,
            patient_condition=request.form.get('patient_condition')
        )
        db.session.add(emergency)
        db.session.commit()
        
        managers = User.query.filter_by(role='blood_bank_manager').all()
        for manager in managers:
            notification = Notification(
                user_id=manager.id,
                title='🚨 New Emergency Request',
                message=f'Emergency request for {emergency.quantity} units of {emergency.blood_type} from {current_user.full_name}'
            )
            db.session.add(notification)
        db.session.commit()
        
        flash('Emergency request created successfully', 'success')
        return redirect(url_for('emergency_requests'))
    
    requests = EmergencyRequest.query.filter_by(hospital_id=current_user.id).order_by(
        EmergencyRequest.request_date.desc()).all()
    return render_template('emergency_requests.html', requests=requests)

@app.route('/emergency_requests/cancel/<int:request_id>', methods=['POST'])
@login_required
@role_required('hospital_admin')
def cancel_emergency_request(request_id):
    try:
        emergency = EmergencyRequest.query.get_or_404(request_id)
        
        # Check if user owns this request
        if emergency.hospital_id != current_user.id:
            return jsonify({'success': False, 'message': 'Unauthorized action'}), 403
        
        emergency.status = 'cancelled'
        db.session.commit()
        
        # Notify blood bank managers about cancellation
        managers = User.query.filter_by(role='blood_bank_manager').all()
        for manager in managers:
            notification = Notification(
                user_id=manager.id,
                title='📋 Request Cancelled',
                message=f'Emergency request #{request_id} for {emergency.quantity} units of {emergency.blood_type} has been cancelled'
            )
            db.session.add(notification)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Request cancelled successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/donor_profile', methods=['GET', 'POST'])
@login_required
@role_required('blood_donor')
def donor_profile():
    donor = Donor.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        donor.blood_type = request.form.get('blood_type')
        donor.age = int(request.form.get('age')) if request.form.get('age') else None
        donor.weight = float(request.form.get('weight')) if request.form.get('weight') else None
        donor.medical_conditions = request.form.get('medical_conditions')
        
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('donor_profile'))
    
    donation_history = Donation.query.filter_by(donor_id=current_user.id).order_by(
        Donation.scheduled_date.desc()).all()
    
    is_eligible = donor.eligibility_status
    if donor.last_donation_date:
        days_since_last = (datetime.now().date() - donor.last_donation_date).days
        if days_since_last < 56:
            is_eligible = False
    
    return render_template('donor_profile.html', donor=donor, donation_history=donation_history, is_eligible=is_eligible)

@app.route('/schedule_donation', methods=['GET', 'POST'])
@login_required
@role_required('blood_donor')
def schedule_donation():
    donor = Donor.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        scheduled_date = datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%d').date()
        
        if scheduled_date <= datetime.now().date():
            flash('Please select a future date', 'danger')
            return redirect(url_for('schedule_donation'))
        
        donation = Donation(
            donor_id=current_user.id,
            scheduled_date=scheduled_date,
            donation_time=datetime.strptime(request.form.get('donation_time'), '%H:%M').time() if request.form.get('donation_time') else None,
            blood_type=donor.blood_type,
            quantity_units=int(request.form.get('quantity_units', 1)),
            notes=request.form.get('notes')
        )
        db.session.add(donation)
        db.session.commit()
        
        notification = Notification(
            user_id=current_user.id,
            title='Donation Scheduled',
            message=f'Your blood donation has been scheduled for {scheduled_date.strftime("%B %d, %Y")}.'
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('Donation scheduled successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('schedule_donation.html', donor=donor, datetime=datetime, timedelta=timedelta)

@app.route('/donations/complete/<int:donation_id>', methods=['POST'])
@login_required
@role_required('blood_bank_manager')
def complete_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    donation.status = 'completed'
    
    donor = Donor.query.filter_by(user_id=donation.donor_id).first()
    if donor:
        donor.last_donation_date = donation.scheduled_date
        donor.total_donations += 1
    
    inventory = Inventory.query.filter_by(blood_type=donation.blood_type).first()
    if inventory:
        inventory.quantity_units += donation.quantity_units
        inventory.updated_by = current_user.id
    
    db.session.commit()
    
    notification = Notification(
        user_id=donation.donor_id,
        title='Donation Completed',
        message=f'Thank you for your donation! You have saved lives.'
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('Donation marked as completed', 'success')
    return redirect(url_for('dashboard'))

@app.route('/inventory', methods=['GET', 'POST'])
@login_required
@role_required('blood_bank_manager')
def inventory_management():
    if request.method == 'POST':
        for blood_type in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
            quantity_key = f'quantity_{blood_type.replace("+", "_plus").replace("-", "_minus")}'
            quantity = int(request.form.get(quantity_key, 0))
            inventory = Inventory.query.filter_by(blood_type=blood_type).first()
            if inventory:
                inventory.quantity_units = quantity
                inventory.updated_by = current_user.id
        
        db.session.commit()
        flash('Inventory updated successfully', 'success')
        return redirect(url_for('inventory_management'))
    
    inventory = Inventory.query.order_by(Inventory.blood_type).all()
    return render_template('inventory.html', inventory=inventory)

@app.route('/api/respond_request/<int:request_id>', methods=['POST'])
@login_required
@role_required('blood_bank_manager')
def respond_request(request_id):
    emergency = EmergencyRequest.query.get_or_404(request_id)
    inventory = Inventory.query.filter_by(blood_type=emergency.blood_type).first()
    
    if not inventory:
        return jsonify({'success': False, 'message': 'Inventory record not found'})
    
    if inventory.quantity_units >= emergency.quantity:
        inventory.quantity_units -= emergency.quantity
        emergency.status = 'fulfilled'
        emergency.fulfillment_date = datetime.utcnow()
        db.session.commit()
        
        notification = Notification(
            user_id=emergency.hospital_id,
            title='✅ Request Fulfilled',
            message=f'Your emergency request for {emergency.quantity} units of {emergency.blood_type} blood has been fulfilled.'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Request fulfilled successfully'})
    else:
        return jsonify({'success': False, 'message': f'Insufficient inventory. Only {inventory.quantity_units} units available.'})

@app.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(
        Notification.created_at.desc()).all()
    
    for notification in notifications:
        if not notification.is_read:
            notification.is_read = True
    db.session.commit()
    
    return render_template('notifications.html', notifications=notifications)

@app.route('/api/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/unread_notifications_count')
@login_required
def unread_notifications_count():
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'count': count})

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    results = []
    
    if current_user.role == 'blood_bank_manager':
        results = EmergencyRequest.query.filter(
            EmergencyRequest.patient_name.contains(query) |
            EmergencyRequest.blood_type.contains(query)
        ).limit(10).all()
    elif current_user.role == 'hospital_admin':
        results = EmergencyRequest.query.filter_by(hospital_id=current_user.id).filter(
            EmergencyRequest.patient_name.contains(query) |
            EmergencyRequest.blood_type.contains(query)
        ).all()
    
    return render_template('search_results.html', results=results, query=query)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
            
            # Check if inventory exists, if not, create it
            if Inventory.query.count() == 0:
                default_inventory = [
                    Inventory(blood_type='A+', quantity_units=25, critical_threshold=10),
                    Inventory(blood_type='A-', quantity_units=10, critical_threshold=5),
                    Inventory(blood_type='B+', quantity_units=20, critical_threshold=10),
                    Inventory(blood_type='B-', quantity_units=8, critical_threshold=5),
                    Inventory(blood_type='AB+', quantity_units=5, critical_threshold=3),
                    Inventory(blood_type='AB-', quantity_units=3, critical_threshold=2),
                    Inventory(blood_type='O+', quantity_units=30, critical_threshold=15),
                    Inventory(blood_type='O-', quantity_units=15, critical_threshold=8)
                ]
                for item in default_inventory:
                    db.session.add(item)
                db.session.commit()
                print("Default inventory created!")
        except Exception as e:
            print(f"Error creating database: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)