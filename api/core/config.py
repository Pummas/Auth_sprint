from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    DB: str = Field('postgresql', env='DB')
    DB_USER: str = Field('user', env='DB_USER')
    DB_PASSWORD: str = Field('123qwe', env='DB_PASSWORD')
    DB_HOST: str = Field('localhost', env='DB_HOST')
    DB_PORT: int = Field(5432, env='DB_PORT')
    DB_NAME: str = Field('users_jwt_base', env='DB_NAME')

    FLASK_HOST: str = Field('0.0.0.0', env='FLASK_HOST')
    FLASK_PORT: int = Field(5001, env='FLASK_PORT')

    REDIS_HOST = Field('localhost', env='REDIS_HOST')
    REDIS_PORT = Field(6379, env='REDIS_PORT')


app = Flask(__name__)
config = Config()
DB_URL = f'{config.DB}+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}'  # noqa:E501
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
