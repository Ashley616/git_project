from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from CONFIG import DatabaseConfig
from flask_restful import Api


api = Api()
db = SQLAlchemy()

def create_app(name):
    app = Flask(name)
    app.config.from_object(DatabaseConfig)
    db.init_app(app)
    api.init_app(app)
    return app


