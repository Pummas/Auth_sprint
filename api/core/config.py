import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    DB: str = os.getenv('DB', 'postgresql')
    DB_USER: str = os.getenv('DB_USER', 'user')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '123qwe')
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_NAME: str = os.getenv('DB_NAME', 'users_jwt_base')
    psy = f'{DB}+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    DB_URL: str = psy

    FLASK_HOST: str = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT: int = int(os.getenv('FLASK_PORT', 5001))

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
