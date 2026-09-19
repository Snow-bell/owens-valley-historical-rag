# Project Report — Owens Valley Historical Research Assistant

---

## Corpus Design

The corpus consists of 700+ documents spanning primary and secondary historical sources curated for geographic and temporal relevance to the Owens Valley region.

### Source Tiers

| Tier | Description |
|------|-------------|
| 1 | Direct indigenous voices — ethnographies, OVIWC documents, Teri Red Owl |
| 2 | Period primary and local sources — newspapers, local histories, owensvalleyhistory.com |
| 3 | Secondary and reference sources — academic geography, government surveys |

### Bias Taxonomy

Every source carries a bias tag and severity level surfaced alongside every retrieval.

| Tag | Description |
|-----|-------------|
| `primary_indigenous` | Living or direct indigenous voice |
| `academic` | Systematic outside observer with methodological framework |
| `settler_bias` | Written from a settler worldview that marginalizes indigenous experience |
| `institutional_bias` | Produced by or in service of an institution with a stake in the outcome |
| `none` | Factual record with no clear perspective agenda |

Severity is classified as `none`, `mild`, `moderate`, or `severe`.

Full source registry with descriptions: [`src/corpus_registry.py`](src/corpus_registry.py)

### Crawling

owensvalleyhistory.com was crawled selectively using `src/crawl.py`. The Mt. Whitney Pack Trains section (1940s-1970s) was excluded as outside the project's historical scope. The crawler saves pages and PDFs locally as a one-time operation — subsequent runs skip already-saved files.

---

## Design Decisions

### Source bias tagging

Historical sources on the Owens Valley water conflict represent fundamentally opposed perspectives. LA newspapers framed water acquisition as civic progress while indigenous voices described the same events as dispossession. Rather than resolving these contradictions the system surfaces them. Every retrieved chunk carries its source's bias tag and severity level, and the generation prompt instructs the model to flag conflicting perspectives rather than arbitrarily adopting one.

### Curated corpus over broad crawling

Core corpus documents were selected and tiered manually rather than scraped broadly. This prioritizes retrieval precision over recall. A chunk from a relevant primary source outperforms ten chunks from tangentially related material. Chapter-level selection was applied to multi-chapter references to reduce noise from geographically irrelevant content.

### Cohere rerank

Initial retrieval uses ChromaDB cosine similarity to find candidate chunks. A Cohere cross-encoder then reranks those candidates by relevance to the specific query before passing to generation. Cross-encoders evaluate the query and chunk together rather than independently, producing more accurate relevance scores than embedding similarity alone. This replaced an earlier source diversity filter and improved overall scores from 4.59 to 4.82.

### Local vector storage

ChromaDB runs locally with no external dependencies. The corpus contains sensitive historical material including indigenous primary sources. Keeping embeddings and retrieval entirely local avoids sending that content to third-party infrastructure beyond the generation API calls.

### Temperature 0.2 for generation, 0.0 for judgment

Generation uses a low but non-zero temperature to allow natural language variation in answers while staying grounded. The judge uses temperature 0.0 because scoring should be deterministic — the same answer should receive the same score on every run.

---

## Evaluation Methodology

Answer quality is scored automatically on four dimensions using a second LLM call with temperature 0.0:

| Dimension | What it measures |
|-----------|-----------------|
| Contextual alignment | How well the answer addresses the specific question |
| Source faithfulness | Whether claims are traceable to retrieved passages |
| Specificity | Whether details are concrete and particular vs. generic |
| Bias handling | Whether the answer surfaces or accounts for source bias |

Each dimension is scored 1-5. The judge receives the query, the full answer, and the retrieved chunks with bias metadata embedded in each source header.

The test suite consists of 50 domain-specific queries covering Paiute life, water rights history, landscape and geology, settler communities, and railroad history. Queries were designed to stress different corpus tiers and surface known coverage gaps.

### Regression testing

`src/regression.py` compares current eval results against a stored baseline and flags any dimension that drops more than 0.3 points. Exit code 0 on pass, 1 on failure — suitable for CI/CD integration.

---

## Results Over Time

| Run | Model | Retrieval | Overall | Notes |
|-----|-------|-----------|---------|-------|
| Initial | GPT-4o-mini | Cosine similarity | 4.59 / 5 | 50 queries, pre-rerank |
| Post-rerank | GPT-4o-mini | Cohere rerank | 4.82 / 5 | Same 50 queries |
| Model comparison | Mistral 7B | Cohere rerank | 3.50 / 5 | Local inference via Ollama |

### Model comparison findings

| Dimension | GPT-4o-mini | Mistral 7B | Delta |
|-----------|-------------|------------|-------|
| Contextual alignment | 5.00 | 3.34 | -1.66 |
| Source faithfulness | 4.96 | 3.88 | -1.08 |
| Specificity | 4.92 | 3.52 | -1.40 |
| Bias handling | 4.40 | 3.24 | -1.16 |
| Overall | 4.82 | 3.50 | -1.32 |

Mistral 7B scored meaningfully lower across all dimensions. The gap was largest on contextual alignment, suggesting the smaller model struggles to synthesize retrieved passages into a focused answer. Source faithfulness also dropped, indicating Mistral does not follow the system prompt instruction to answer only from provided sources as reliably as GPT-4o-mini.

Query 47 — "Describe the living conditions at the Fort Tejon reservation during the Paiute forced relocation" — produced significant latency on Mistral 7B. Fort Tejon lies outside the corpus's geographic scope, resulting in low-relevance retrieval. Mistral appeared to generate from parametric knowledge rather than the retrieved passages, which is the hallucination risk RAG is designed to mitigate. GPT-4o-mini handled this case better, more consistently declining to answer when retrieved context was insufficient.

---

## Known Limitations

- The LLM judge uses the same model as generation (GPT-4o-mini). This introduces self-evaluation bias — the model tends to score its own outputs favorably. A stronger judge model would produce more reliable scores in production.
- Corpus coverage of Paiute spiritual and religious practices is sparse. Queries on this topic return insufficient context.
- Transliteration of Paiute language terms varies across corpus documents from different eras. Queries about specific terminology may surface variant spellings depending on which sources are retrieved.
- Ghosts of the Sagebrush is primarily a photo document. Extracted text is fragmentary and retrieved chunks should be treated as partial context only.
- OCR preprocessing is not implemented. All corpus documents must be text-selectable PDFs.
- Mistral 7B inference runs on CPU on AMD hardware without ROCm configuration, producing query latency of approximately 51 seconds per query.

---

## Future Work

- Multimodal ingestion of historical maps and photographs via vision model description pipeline
- Evaluate Anthropic Claude as an alternative generation model for nuanced historical prose synthesis
- Stronger judge model (GPT-4o) to reduce self-evaluation bias
- Expanded owensvalleyhistory.com crawl coverage
- Visualization of evaluation scores across query dimensions and runs
- ROCm configuration for AMD GPU acceleration of local inference