
from dotenv import load_dotenv
import os

load_dotenv()


WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
if not WEBHOOK_SECRET:
    print("Warning: WEBHOOK_SECRET is not set in environment variables.")
    exit(1)
WEBHOOK_SECRET = str(WEBHOOK_SECRET)

APP_ID = os.getenv("APP_ID")
if not APP_ID:
    print("Warning: APP_ID is not set in environment variables.")
    exit(1)
APP_ID = str(APP_ID)

PRIVATE_KEY_FILE = os.getenv("PRIVATE_KEY_FILE")
if not PRIVATE_KEY_FILE:
    print("Warning: PRIVATE_KEY_FILE is not set in environment variables.")
    exit(1)
PRIVATE_KEY_FILE = str(PRIVATE_KEY_FILE)

try:
    with open(str(os.getenv("PRIVATE_KEY_FILE")), "r") as key_file:
        PRIVATE_KEY = key_file.read()
except Exception as e:
    print(f"Error reading PRIVATE_KEY_FILE: {e}")
    exit(1)
PRIVATE_KEY = str(PRIVATE_KEY)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set in environment variables.")
    exit(1)
GEMINI_API_KEY = str(GEMINI_API_KEY)
