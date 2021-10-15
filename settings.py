import os 
from dotenv import load_dotenv

load_dotenv()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = str(os.getenv("ENGINE_DB"))
    SQLALCHEMY_TRACK_MODIFICATIONS = True