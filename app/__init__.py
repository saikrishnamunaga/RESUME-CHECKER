"""Application factory and blueprint registration."""
import os
from flask import Flask, render_template
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.google import make_google_blueprint
from werkzeug.security import generate_password_hash
from .extensions import db, migrate, login_manager, csrf
from .models import User


def _seed_default_test_user(app: Flask) -> None:
    """Create a default test user with known credentials for local testing."""
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='test@gmail.com').first():
            user = User(
                name='Test User',
                email='test@gmail.com',
                password_hash=generate_password_hash('Password123!'),
            )
            db.session.add(user)
            db.session.commit()


def create_app(config_object) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_object: Config subclass or config object.

    Returns:
        Configured Flask app.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static'),
        instance_relative_config=False,
    )
    app.config.from_object(config_object)

    if app.config.get('DEBUG'):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    if app.config.get('GOOGLE_OAUTH_CLIENT_ID') and app.config.get('GOOGLE_OAUTH_CLIENT_SECRET'):
        google_bp = make_google_blueprint(
            client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
            client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
            scope=['profile', 'email'],
            redirect_to='auth.google_login',
        )
        app.register_blueprint(google_bp, url_prefix='/auth/google')

    if app.config.get('FACEBOOK_OAUTH_CLIENT_ID') and app.config.get('FACEBOOK_OAUTH_CLIENT_SECRET'):
        facebook_bp = make_facebook_blueprint(
            client_id=app.config['FACEBOOK_OAUTH_CLIENT_ID'],
            client_secret=app.config['FACEBOOK_OAUTH_CLIENT_SECRET'],
            scope=['email'],
            redirect_to='auth.facebook_login',
        )
        app.register_blueprint(facebook_bp, url_prefix='/auth/facebook')

    # Register blueprints
    from .blueprints.main import main_bp
    from .blueprints.auth import auth_bp
    from .blueprints.dashboard import dashboard_bp
    from .blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    _seed_default_test_user(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app
