from flask_app import app
from flask import render_template, redirect, session, request, flash, abort, url_for
from functools import wraps
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
from datetime import timedelta, datetime
import pytz

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            abort(403)
        user_id = session['user_id']
        loggedAdmin = User.is_admin(user_id) 
        if not loggedAdmin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    admin_data = {
        'username': 'Admin User',
        'role': 'admin',
    }
    vehicles = Vehicle.getAllVehicles()
    return render_template('admin_dashboard.html', loggedAdmin=admin_data,vehicles = vehicles)