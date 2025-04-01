import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_url = os.environ.get("DATABASE_URL", "").replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-guess")
    SQLALCHEMY_DATABASE_URI = db_url if db_url else f"sqlite:///{os.path.join(basedir, 'attention_test.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
