from flask import Flask
from app.register import register
from settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register(app)
    return app

def register_extensions(app):
    from app.extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

app = create_app()