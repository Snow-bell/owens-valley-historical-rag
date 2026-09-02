# Owens Valley Historical Research Assistant

A domain-specific RAG (Retrieval-Augmented Generation) pipeline for querying 
primary and secondary historical sources about the Owens Valley region of 
California circa 1880–1915. Built to support historical fiction research with 
period-accurate context retrieval and source bias transparency.

---

## Overview

This tool allows a writer to ask natural language research questions and receive 
grounded answers drawn exclusively from a curated corpus of historical documents. 
Every answer is accompanied by source citations and bias warnings, enabling 
critical evaluation of retrieved content before use in creative work. This tool retrieves and synthesizes historical context. Answers are grounded strictly in source passages.

**Example queries:**
- *What did Paiute families eat during winter months?*
- *How did Los Angeles justify the acquisition of Owens Valley water rights?*
- *Describe the landscape of the Owens Valley floor in early spring.*

---

## Architecture

**Query pipeline**
```
Query (CLI)
    ↓
retrieve.py   — embeds query, finds top-k similar chunks via ChromaDB
    ↓
generate.py   — sends retrieved chunks + query to GPT-4o-mini
    ↓
main.py       — handles CLI interaction, surfaces answer and bias warnings
```

**Evaluation pipeline**
```
evaluate.py   — runs predefined test queries through full pipeline
    ↓
judge.py      — scores each answer on 4 dimensions via LLM-as-judge
    ↓
outputs/eval_results.csv
```

---

## Corpus

The corpus consists of 40+ primary and secondary source documents curated for 
geographic and temporal relevance to the Owens Valley region, 1880–1915. Sources 
span three tiers — direct indigenous voices, period primary sources, and secondary 
reference material — each tagged with a bias classification and severity level.

Full source registry with descriptions: [`src/corpus_registry.py`](src/corpus_registry.py)

---

## Setup

### Requirements
- Python 3.10+
- OpenAI API key

### Installation

```bash
git clone https://github.com/YOURUSERNAME/owens-valley-historical-rag.git
cd owens-valley-historical-rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_key_here
```

### Add corpus documents

Place your PDF corpus documents in `data/corpus/`, maintaining the subfolder 
structure for `chronicling-america/` and `womens-club-biographies/`.

---

## Usage

### First run — index the corpus

```bash
python main.py
```

The corpus is indexed automatically on first run. To force reindexing after 
adding new documents:

```bash
python main.py --reindex
```

### Query the corpus

Once indexed, the tool enters an interactive query loop:
```
Research question: What did Paiute families eat during winter months?
```

Every answer includes cited sources with bias warnings.

### Run evaluation

```bash
python -m src.evaluate
```

Results saved to `outputs/eval_results.csv`.

---

## Design Decisions

### Source bias tagging
Historical sources on the Owens Valley water conflict represent fundamentally 
opposed perspectives — LA newspapers framing water acquisition as civic progress, 
indigenous voices describing the same events as dispossession. Rather than 
resolving these contradictions, the system surfaces them. Every retrieved chunk 
carries its source's bias tag and severity level, and the generation prompt 
instructs the model to flag conflicting perspectives rather than arbitrarily 
adopting one.

### Curated corpus over broad crawling
Corpus documents were selected and tiered manually rather than scraped broadly. 
This prioritizes retrieval precision over recall — a chunk from a relevant primary 
source outperforms ten chunks from tangentially related material. Chapter-level 
selection was applied to multi-chapter references to reduce noise from 
geographically irrelevant content.

### LLM-as-judge evaluation
Answer quality is scored automatically on four dimensions — contextual alignment, 
source faithfulness, specificity, and bias handling — using a second GPT-4o-mini 
call with temperature 0.0 for deterministic scoring. This removes subjective 
manual scoring and enables systematic comparison across query types.

### Local vector storage
ChromaDB runs locally with no external dependencies. The corpus contains 
sensitive historical material including indigenous primary sources — keeping 
embeddings and retrieval entirely local avoids sending that content to 
third-party infrastructure beyond the generation API calls.

### Temperature 0.2 for generation, 0.0 for judgment
Generation uses a low but non-zero temperature to allow natural language 
variation in answers while staying grounded. The judge uses temperature 0.0 
because scoring should be deterministic — the same answer should receive the 
same score on every run.

---

## Known Limitations

- **Ghosts of the Sagebrush** is primarily a photo document — extracted text 
  is fragmentary and retrieved chunks should be treated as partial context only.
- OCR preprocessing is not implemented. All corpus documents must be 
  text-selectable PDFs.
- The LLM judge uses the same model as generation (GPT-4o-mini). In production, 
  a stronger judge model would produce more reliable evaluation scores.
- Corpus coverage is limited to documents available in the public domain or 
  personally sourced. owensvalleyhistory.com is not yet crawled.

---

## Future Work

- Web crawler for owensvalleyhistory.com primary source collection
- Multimodal ingestion of historical maps and photographs via vision model 
  description pipeline
- Evaluate Anthropic Claude as alternative generation model for nuanced 
  historical prose synthesis
- Expanded corpus coverage beyond 1880–1915
- Visualization of evaluation scores across query dimensions

---

## License

MIT
