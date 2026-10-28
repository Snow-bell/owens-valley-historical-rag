# Owens Valley Historical Research Assistant

A retrieval-augmented generation (RAG) pipeline for researching the Owens Valley region of California, circa 1880–1930. It answers questions from about 650 primary and secondary sources: settler histories, Paiute ethnographies and life stories, 1900s Los Angeles newspapers, USGS reports, Paiute institutional histories and several hundred local history pages from owensvalleyhistory.com. It was built to give a historical fiction writer period-accurate context without hiding whose perspective each source carries.

Answers are grounded only in retrieved passages and cite them by title and printed page, for example (The Story of Inyo, p. 32). The tool retrieves and synthesizes historical context; it does not write prose.

The sources disagree, often sharply. The Los Angeles Herald presented the aqueduct as civic progress; Paiute sources describe the same years as dispossession; the main county history is written from a settler perspective with racist language. The pipeline surfaces this at two levels: every document carries a bias tag in a curated registry, and every passage carries a stance label made when the corpus is indexed.

For methodology, evaluation results and design decisions, see [REPORT.md](REPORT.md).

---

## How it works

**Indexing** (`python main.py --reindex`)
```
ingest.py      PDFs read page by page, with registry page ranges for long books;
               running heads and page numbers stripped; printed page numbers kept
               for citations; text cleaned (paragraphs, hyphenated words, OCR noise)
   ↓
chunk.py       semantic chunking: sentences (NLTK) embedded locally with MiniLM and
               split where the topic changes, 300–800 tokens per chunk
   ↓
stance.py      GPT-4.1-mini labels each chunk's stance toward the Paiute, Los Angeles
               and the settlers, its loaded terms and its framing; cached by chunk text
   ↓
embed.py       each chunk embedded (OpenAI text-embedding-3-small) with a header naming
               its source (title · author · year · type), stored in ChromaDB
```

**Answering a question** (`python main.py`)
```
retrieve.py    the 50 chunks closest to the question in ChromaDB
   ↓
rerank.py      Cohere rerank-english-v3.0 picks the 5 most relevant
   ↓
generate.py    GPT-4o-mini answers from those 5 passages, each labeled with its title,
               pages, bias tag and stance; cites title and page, names opposing stances
   ↓
main.py        prints the answer, the sources with their pages and bias warnings, and
               with --verbose each passage's stance labels
```

**Evaluation** (`python -m src.evaluate`)
```
evaluate.py    runs 50 test questions through the full pipeline and saves every answer
   ↓
judge.py       Gemma 3 12B, running locally through Ollama, scores each answer 1–5 on
               contextual alignment, source faithfulness, specificity and bias handling
   ↓
regression.py  compares a run with a baseline and flags any dimension that drops by 0.3
```

---

## Results

Each change was measured on its own against the run before it, with the same judge (`gemma3:12b`, prompt v2). Scores are averages over the 50 test questions.

| Run | Change | Specificity | Bias handling | Overall |
|-----|--------|-------------|---------------|---------|
| Baseline | Fixed 800-token chunks, 15k-character document cap | 4.78 | 3.80 | 4.64 |
| B1 | Page-by-page extraction, page ranges, text cleanup | 4.90 | 3.80 | 4.67 |
| B2 | Semantic chunking | 4.86 | 3.72 | 4.65 |
| B3 | Reranking 50 candidates instead of 15 | 4.88 | 3.84 | 4.68 |
| B4 | Source headers on each chunk | 4.90 | 3.90 | 4.70 |

Contextual alignment and source faithfulness are at or near 5.00 in every run, so they work as checks for a collapse rather than as measures of improvement. Bias handling is the weakest dimension and the one the stance labels target. See [REPORT.md](REPORT.md) for per-question changes, retrieval statistics and known limitations.

---

## Setup

### Requirements

- Python 3.10+
- OpenAI API key (embeddings, generation, stance labels)
- Cohere API key (reranking; a free trial key works, paced to 10 calls a minute)
- [Ollama](https://ollama.com) with `gemma3:12b`, for evaluation only. It needs about 8 GB of GPU memory. To judge with GPT-4o-mini instead, set `JUDGE_PROVIDER = "openai"` in `src/config.py`.

### Installation

```bash
git clone https://github.com/Snow-bell/owens-valley-historical-rag.git
cd owens-valley-historical-rag
python -m venv .venv
source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

The `pip install torch` line installs the CPU-only PyTorch build that `sentence-transformers` needs for semantic chunking; without it, pip pulls the much larger CUDA build. NLTK's `punkt_tab` sentence data and the MiniLM model download on first use.

For evaluation, install Ollama and pull the judge model:

```bash
ollama pull gemma3:12b
```

### Configuration

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
```

Every other setting is in [src/config.py](src/config.py): the chunking method and sizes, the number of rerank candidates, the generation, stance and judge models.

### Add corpus documents

The corpus isn't distributed with the repo. Place PDF documents in `data/corpus/`, with the `chronicling-america/` and `womens-club-biographies/` subfolders. Each document's tier, bias tag, title, author, year and page ranges are set in [src/corpus_registry.py](src/corpus_registry.py); crawled pages share a default entry.

To crawl owensvalleyhistory.com into `data/corpus/owensvalleyhistory/`:

```bash
python -m src.crawl
```

---

## Usage

### Index the corpus

```bash
python main.py --reindex
```

`python main.py` indexes automatically if no index exists. `--reindex` rebuilds the collection from scratch, so chunks from deleted or changed documents don't linger. A full reindex takes about 15 minutes, most of it MiniLM on the CPU.

- **Chunking method.** `CHUNK_METHOD` in `src/config.py` picks `semantic` (the default, collection `owens_valley_semantic`) or `fixed` (800-token windows, collection `owens_valley`). Each method has its own collection, and reindexing one leaves the other intact, so the two can be compared.
- **Stance labels.** The first reindex labels every chunk with `STANCE_MODEL` (GPT-4.1-mini, about $2 for the full corpus). Labels are cached in `data/stance_cache.json` by chunk text, so later reindexes only label chunks whose text changed. Set `STANCE_LABELS = False` to index without them.

### Ask questions

Once indexed, the tool opens an interactive loop:
```
Research question: What did Paiute families eat during winter months?
```

Each answer is followed by its sources: title, cited pages, tier and any bias warning from the registry. To also see each retrieved passage's stance toward the Paiute, Los Angeles and the settlers, its loaded terms and its framing:

```bash
python main.py --verbose
```

### Run an evaluation

```bash
python -m src.evaluate --model openai    # GPT-4o-mini answers
python -m src.evaluate --model mistral   # Mistral 7B through Ollama
```

Scores go to `outputs/eval_results_<model>.csv`, and full answers with their retrieved chunks to `outputs/eval_answers_<model>.jsonl`. Runs against the semantic collection add its name to both file names, for example `eval_results_openai__owens_valley_semantic.csv`.

### Re-score saved answers

Re-runs only the judge on a saved run, without retrieving or generating again. Choose the judge with `JUDGE_PROVIDER` (`"ollama"` or `"openai"`) and `JUDGE_MODEL` in `src/config.py`.

```bash
python -m src.evaluate --rejudge eval_answers_openai.jsonl
```

Results go to `outputs/eval_results_<model>__judge_<judge>.csv`, where `<judge>` is the judge model plus its prompt version, for example `gemma3_12b@v2`.

### Check for regressions

```bash
python -m src.regression --baseline b3_openai_gemma-v2-judge.csv --current b4_openai_gemma-v2-judge.csv
```

Both files are read from `outputs/`. Any dimension that drops by more than 0.3 fails the check. Runs scored by different judge models or prompt versions are refused, since their scores aren't comparable.

### Compare GPT-4o-mini with Mistral 7B

```bash
python -m src.compare
```

Compares `eval_results_openai.csv` with `eval_results_mistral.csv`, dimension by dimension.

### Run the tests

```bash
pytest -q
```

All API clients are mocked, so the tests make no network calls.

---

## License

MIT
