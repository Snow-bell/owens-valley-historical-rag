import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
CORPUS_DIR = BASE_DIR / "data" / "corpus"
CHROMA_DIR = BASE_DIR / "data" / "chroma"
OUTPUTS_DIR = BASE_DIR / "outputs"

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o-mini"

# Generation parameters
TEMPERATURE = 0.2
TOP_P = 0.9
MAX_TOKENS = 1000

# Chunking
CHUNK_SIZE = 500        # tokens per chunk
CHUNK_OVERLAP = 50      

# Retrieval
TOP_K = 5               

# Collection
CHROMA_COLLECTION = "owens_valley"