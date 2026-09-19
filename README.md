# Owens Valley Historical Research Assistant

A domain-specific RAG pipeline for querying 700+ primary and secondary historical sources about the Owens Valley region of California. Built to support historical fiction research with period-accurate context retrieval and source bias transparency.

Answers are grounded strictly in retrieved source passages. This tool retrieves and synthesizes historical context; it does not generate prose.

For full methodology, evaluation results, and design decisions see [REPORT.md](REPORT.md).

---

## Architecture

**Query pipeline**
```
Query (CLI)
↓
retrieve.py — embeds query, finds candidates via ChromaDB, reranks via Cohere
↓
generate.py — sends reranked chunks + query to GPT-4o-mini or Mistral 7B
↓
main.py — handles CLI interaction, surfaces answer and bias warnings
```

**Evaluation pipeline**
```
evaluate.py — runs 50 test queries through the full pipeline
↓
judge.py — scores each answer on 4 dimensions via LLM-as-judge
↓
outputs/eval_results_<model>.csv
```

---

## Setup

### Requirements

- Python 3.10+
- OpenAI API key
- Cohere API key
- Ollama (optional, for local Mistral 7B inference)

### Installation

```bash
git clone https://github.com/Snow-bell/owens-valley-historical-rag.git
cd owens-valley-historical-rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
```

### Add corpus documents

Place PDF corpus documents in `data/corpus/`, maintaining subfolder structure for `chronicling-america/` and `womens-club-biographies/`.

To crawl owensvalleyhistory.com:

```bash
python -m src.crawl
```

---

## Usage

### Index the corpus

```bash
python main.py
```

Indexes automatically on first run. To force reindex:

```bash
python main.py --reindex
```

### Query the corpus

Once indexed the tool enters an interactive query loop:
```
Research question: What did Paiute families eat during winter months?
```

### Run evaluation

```bash
# OpenAI (default)
python -m src.evaluate --model openai

# Mistral 7B via Ollama
python -m src.evaluate --model mistral
```

Results saved to `outputs/eval_results_<model>.csv`.

### Compare models

```bash
python -m src.compare
```

### Run regression check

```bash
python -m src.regression --baseline eval_results_openai.csv --current eval_results_mistral.csv
```

---

## License

MIT