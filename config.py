import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL_V3 = "https://catalog.api.2gis.com/3.0"

if not API_KEY:
    raise ValueError("API_KEY не найден!")