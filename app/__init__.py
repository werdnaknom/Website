from flask import Flask
from config import Config
import requests
from flask_wtf import CSRFProtect
from celery import Celery

from flask_bootstrap import Bootstrap

def create_app(config_class=Config):
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    CSRFProtect(app)
    app.config.from_object(config_class)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

