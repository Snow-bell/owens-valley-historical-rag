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
CHUNK_METHOD = "semantic"   # "fixed" (800-token windows) or "semantic"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Semantic chunking: sentences grouped at topic changes
SENTENCE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"   # local, CPU
SEMANTIC_WINDOW = 1              # sentences either side, embedded with each sentence
SEMANTIC_BREAK_PERCENTILE = 95   # break above this percentile of all neighbour distances in the corpus
SEMANTIC_MIN_TOKENS = 300        # smaller pieces merge into a neighbour; 300 brings mean size to ~560 tokens (fixed: ~710)
SEMANTIC_MAX_TOKENS = CHUNK_SIZE # same cap as fixed chunks, so B2 against B1 tests only where chunks break
SEMANTIC_OVERLAP_MAX_TOKENS = 100  # the repeated last sentence is skipped if longer

# Ingestion
MAX_CHARS = 600_000   # safety cap per document; long books are trimmed with registry page ranges

# Retrieval
TOP_K = 5        
RERANK_CANDIDATES = 50   # chunks fetched from Chroma for Cohere to rerank; up to 100 still costs one search unit

# Cohere
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
RERANK_MODEL = "rerank-english-v3.0"
RERANK_TOP_N = TOP_K       
COHERE_CALLS_PER_MINUTE = 10    # trial key limit; raise for a production key

# Collection: one per chunk method, so both indexes stay available to compare
CHROMA_COLLECTIONS = {
    "fixed": "owens_valley",
    "semantic": "owens_valley_semantic",
}
DEFAULT_COLLECTION = CHROMA_COLLECTIONS["fixed"]   # runs before collections existed used this one; its output files keep unsuffixed names
CHROMA_COLLECTION = CHROMA_COLLECTIONS[CHUNK_METHOD]

# Regression
REGRESSION_THRESHOLD = 0.3