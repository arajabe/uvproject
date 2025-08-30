from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Database
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@host.docker.internal:{DB_PORT}/{DB_NAME}"
# API
API_URL = os.getenv("API_URL")

# LLM
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_API_KEY = os.getenv("LLM_API_KEY")

# Frontend
FRONTEND_SECRET_KEY = os.getenv("FRONTEND_SECRET_KEY")