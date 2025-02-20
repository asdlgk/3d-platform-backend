from flask import Flask
from flask_redis import FlaskRedis
from .routes import api_blueprint
from .services.autodl import AutoDLClient
