import os
from utils.constants import AppConstants
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY_ID = os.getenv(AppConstants.ENV_ACCESS_KEY_ID)
SECRET_ACCESS_KEY = os.getenv(AppConstants.ENV_SECRET_ACCESS_KEY)
ENDPOINT_URL = os.getenv(AppConstants.ENV_ENDPOINT_URL)
