import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
BASE_URL = os.getenv("BASE_URL")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")