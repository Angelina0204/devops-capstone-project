"""
Account Service application initialization.
"""

import sys

from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Enable Cross-Origin Resource Sharing
CORS(app)

# Enable HTTP security headers
Talisman(app)

# Import application modules after creating the app
from service import routes, models  # noqa: E402, F401
from service.common import error_handlers, cli_commands  # noqa: E402, F401

# Initialize application logging
log_handlers.init_logging(app, "gunicorn.error")

try:
    models.init_db(app)
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Account Service initialized!")
