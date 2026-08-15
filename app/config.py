import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL","https://api.deepseek.com")
DEEPSEEK_MODEL = 'deepseek-v4-flash'

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_docs")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

CHUNK_SIZE = 200
CHUNK_OVERLAP = 30
