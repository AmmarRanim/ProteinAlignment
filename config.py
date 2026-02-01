"""Configuration settings for the protein analysis application"""
import os
try:
	from dotenv import load_dotenv, find_dotenv  # type: ignore
	# Load from current working directory chain
	load_dotenv(find_dotenv(usecwd=True))
	# Also load .env next to this file to be robust to cwd differences
	env_path = os.path.join(os.path.dirname(__file__), '.env')
	if os.path.exists(env_path):
		load_dotenv(env_path, override=False)
except Exception:
	# python-dotenv is optional; environment variables still work without it
	pass

# Chunking parameters
CHUNK_LEN = 10
CHUNK_STRIDE = 5

# Smith-Waterman alignment parameters
GAP_OPEN = -0.2
GAP_EXTEND = -0.1
SCORE_THRESHOLD = 0.5

# Cache directory
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Master parquet files (put your existing files here)
# The app will check these files first before creating new chunks
MASTER_CHUNKS_DIR = "data"  # Your data folder
HUMAN_CHUNKS_FILE = "Homo_sapiens_chunks.parquet"
BACTERIA_CHUNKS_FILE = "Klebsiella_pneumoniae_chunks.parquet"

# Flask settings
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# LLM settings (optional - for AI-powered interpretation)
# Get your free API key at: https://console.groq.com/keys
# Read from environment (.env supported) to avoid committing secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
