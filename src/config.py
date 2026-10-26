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

# Judge
JUDGE_PROVIDER = "ollama"   # "openai" or "ollama"
JUDGE_MODEL = "gemma3:12b" # "gpt-4o-mini" or "gemma3:12b"
JUDGE_NUM_CTX = 16384      # Ollama context window; its default silently truncates the judge prompt

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Ingestion
MAX_CHARS = 600_000   # safety cap per document; long books are trimmed with registry page ranges

# Retrieval
TOP_K = 5        
RERANK_CANDIDATES = TOP_K * 3   # chunks fetched from Chroma for Cohere to rerank

# Cohere
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
RERANK_MODEL = "rerank-english-v3.0"
RERANK_TOP_N = TOP_K       
COHERE_CALLS_PER_MINUTE = 10    # trial key limit; raise for a production key

# Collection
CHROMA_COLLECTION = "owens_valley"

# Regression
REGRESSION_THRESHOLD = 0.3