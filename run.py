"""Application entrypoint for AI Resume Analyzer Pro."""
import os
from app import create_app
from config import config

config_name = os.environ.get('FLASK_ENV', 'default')
app = create_app(config[config_name])

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False),
    )
