import os
from dotenv import load_dotenv

load_dotenv(override=False)

PYTHON_ENV = os.getenv("PYTHON_ENV")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
EMAIL = os.getenv("EMAIL")
DATASET_ID = os.getenv("DATASET_ID")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
USERNAME = os.getenv("USERNAME")
FRAISE = os.getenv("FRAISE")
FA2 = os.getenv("2FA")
INT = os.getenv("INT")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
ALPHA_VENTAGE_API_KEY = os.getenv("ALPHA_VENTAGE_API_KEY")
