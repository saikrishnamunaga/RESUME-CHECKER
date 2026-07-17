from app import create_app
from app.models import User
from config import Config
from werkzeug.security import check_password_hash


def test_import_app():
    # Basic smoke test to ensure package imports
    import importlib
    app = importlib.import_module('app')
    assert hasattr(app, 'create_app')


def test_default_test_user_is_seeded():
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        WTF_CSRF_ENABLED = False

    app = create_app(TestConfig)
    with app.app_context():
        user = User.query.filter_by(email='test@gmail.com').first()
        assert user is not None
        assert check_password_hash(user.password_hash, 'Password123!')
