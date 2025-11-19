import os
from dotenv import load_dotenv

load_dotenv()

# Student credentials
EMAIL = os.getenv("EMAIL", "")
SECRET = os.getenv("SECRET", "")

# Server configuration
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# LLM Provider configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai or iitm
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
IITM_AI_TOKEN = os.getenv("IITM_AI_TOKEN", "")
IITM_API_BASE_URL = os.getenv("IITM_API_BASE_URL", "https://llm.iitm.ac.in/v1")
MODEL = os.getenv("MODEL", "gpt-4-turbo-preview")

# Quiz solving configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "180"))

# File paths
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")

# Create directories if they don't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
