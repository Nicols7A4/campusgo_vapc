import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "campusgo")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "campusgo-clave-secreta-cambiar")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    PROFILE_PHOTO_DIR = os.getenv(
        "PROFILE_PHOTO_DIR",
        os.path.join(BASE_DIR, "uploads", "perfiles")
    )
