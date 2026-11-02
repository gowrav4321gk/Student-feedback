import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")


def get_database_uri():
    """
    Determines the appropriate database URI.
    Supports MySQL via PyMySQL as the primary configuration.
    Provides graceful fallback to SQLite for immediate local testing if MySQL
    credentials are not yet configured or connection fails.
    """
    # 1. Direct DATABASE_URL override if present
    custom_url = os.environ.get("DATABASE_URL")
    if custom_url:
        return custom_url

    db_type = os.environ.get("DB_TYPE", "mysql").lower()

    if db_type == "mysql":
        db_user = os.environ.get("DB_USER", "root")
        db_password = os.environ.get("DB_PASSWORD", "")
        db_host = os.environ.get("DB_HOST", "localhost")
        db_port = os.environ.get("DB_PORT", "3306")
        db_name = os.environ.get("DB_NAME", "student_feedback_db")

        # Quick test to see if MySQL is reachable before returning URI
        # This prevents the app from crashing on first launch if student hasn't started MySQL
        try:
            import pymysql
            connection = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                port=int(db_port),
                connect_timeout=2
            )
            # Create database if it doesn't exist
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            connection.close()

            encoded_password = pymysql.converters.escape_string(db_password) if db_password else ""
            auth = f"{db_user}:{db_password}" if db_password else db_user
            return f"mysql+pymysql://{auth}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
        except Exception as e:
            # Informative message for student/evaluator
            print(f"[Database Config] Notice: MySQL not reachable ({e}).")
            print("[Database Config] Falling back to SQLite for seamless local execution.")

    # SQLite fallback
    instance_dir = BASE_DIR / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)
    sqlite_path = instance_dir / "student_feedback.db"
    return f"sqlite:///{sqlite_path}"


class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "btech-cse-student-feedback-system-secret-key-2025")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    
    # WTForms CSRF protection
    WTF_CSRF_ENABLED = True
    
    # Static folders and upload paths
    STATIC_FOLDER = BASE_DIR / "static"
    TEMPLATES_FOLDER = BASE_DIR / "templates"
    CHARTS_DIR = STATIC_FOLDER / "charts"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
