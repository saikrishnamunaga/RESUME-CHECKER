from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import admin_bp


@admin_bp.route('/')
@login_required
def admin_home():
    if not getattr(current_user, 'is_admin', False):
        flash('Administrator access required.', 'warning')
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template('admin/index.html')
