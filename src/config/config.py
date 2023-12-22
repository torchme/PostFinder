import os
from pathlib import Path
from dotenv import load_dotenv


dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
