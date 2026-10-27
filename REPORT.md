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

### Semantic chunking

Documents are split at topic changes instead of every 800 tokens. Each sentence is embedded locally with MiniLM (all-MiniLM-L6-v2), together with one sentence on either side, and a chunk breaks where the distance between neighbouring sentences is a local peak above the 95th percentile of all such distances in the corpus. One threshold for the whole corpus keeps break density tied to how much the text actually shifts, so a short newspaper article on one subject stays whole while a book splits at its chapter and section changes. Pieces under 300 tokens merge into the previous chunk, pieces over 800 tokens split at their largest internal distance, and each chunk repeats the previous chunk's last sentence for continuity.

The 800-token maximum matches the fixed chunker, so comparing the two tests where chunks break rather than how much text the generator sees. Semantic chunks still come out smaller (mean about 560 tokens against 710) because they end at topic changes: with a 100-token minimum the mean was 412 tokens and the generator would have seen 58% of the fixed chunker's context, so the minimum was raised to 300, giving about 80%.

Semantic chunking scored 4.65 against 4.67 for fixed chunks on the same extraction (runs B1 and B2 below), a tie within noise, while giving the generator 20% less text. It is the default because chunks that hold one topic are a better unit for what comes next: per-chunk sentiment scoring, contextual chunk headers and page citations. The fixed-chunk collection is kept for comparison.

### Local vector storage

ChromaDB runs locally with no external dependencies. The corpus contains sensitive historical material including indigenous primary sources. Keeping embeddings and retrieval entirely local avoids sending that content to third-party infrastructure beyond the generation API calls.

### Temperature 0.2 for generation, 0.0 for judgment

Generation uses a low but non-zero temperature to allow natural language variation in answers while staying grounded. The judge uses temperature 0.0 because scoring should be deterministic — the same answer should receive the same score on every run.

---

## Evaluation Methodology

Answer quality is scored automatically on four dimensions by a separate judge model at temperature 0.0. The judge is Gemma 3 12B, run locally through Ollama on the GPU, so it is a different model from the GPT-4o-mini generator. Earlier runs used GPT-4o-mini as the judge.

| Dimension | What it measures |
|-----------|-----------------|
| Contextual alignment | How well the answer addresses the specific question |
| Source faithfulness | Whether claims are traceable to retrieved passages |
| Specificity | Whether details are concrete and particular vs. generic |
| Bias handling | Whether the answer surfaces or accounts for source bias |

Each dimension is scored 1-5. The judge receives the query, the full answer, and the retrieved chunks with bias metadata embedded in each source header. Ollama constrains the reply to a JSON schema; scores must be whole numbers from 1 to 5, and an invalid reply is retried once.

Every results row records the judge as model plus prompt version (for example `gemma3:12b@v2`). Scores are only comparable within one judge model and prompt version, and the regression check refuses to compare runs that differ. Full answers are saved with each run, so a run can be rescored by a new judge without generating again.

The test suite consists of 50 domain-specific queries covering Paiute life, water rights history, landscape and geology, settler communities, and railroad history. Queries were designed to stress different corpus tiers and surface known coverage gaps.

### Regression testing

`src/regression.py` compares current eval results against a stored baseline and flags any dimension that drops more than 0.3 points. Exit code 0 on pass, 1 on failure — suitable for CI/CD integration.

---

## Results Over Time

| Run | Model | Retrieval | Judge | Overall | Notes |
|-----|-------|-----------|-------|---------|-------|
| Initial | GPT-4o-mini | Cosine similarity | GPT-4o-mini | 4.59 / 5 | 50 queries, pre-rerank |
| Post-rerank | GPT-4o-mini | Cohere rerank | GPT-4o-mini | 4.82 / 5 | Same 50 queries |
| Model comparison | Mistral 7B | Cohere rerank | GPT-4o-mini | 3.50 / 5 | Local inference via Ollama |
| Corpus cleanup | GPT-4o-mini | Cohere rerank | GPT-4o-mini | 4.75 / 5 | Seven junk crawl files removed; new answers |
| Judge switch | GPT-4o-mini | Cohere rerank | Gemma 3 12B, prompt v1 | 4.59 / 5 | Same answers as corpus cleanup, rescored |
| Judge prompt v2 | GPT-4o-mini | Cohere rerank | Gemma 3 12B, prompt v2 | 4.64 / 5 | Same answers, rescored; baseline for B1 |
| B1: new extraction | GPT-4o-mini | Cohere rerank | Gemma 3 12B, prompt v2 | 4.67 / 5 | Page ranges, header stripping, text cleanup; fixed 800-token chunks (3,389) |
| B2: semantic chunks | GPT-4o-mini | Cohere rerank | Gemma 3 12B, prompt v2 | 4.65 / 5 | Same extraction, semantic chunks (3,847); current default |

Scores from different judges are not comparable. The judge switch and prompt v2 rows score the same 50 answers as the corpus cleanup row, so their differences come from the judge alone.

B2 against B1 isolates the chunking change. Only 15 of 50 answers changed score on any dimension, in both directions (specificity 3 up and 5 down, bias handling 5 up and 8 down), and alignment and faithfulness stayed at 5.00 in both runs. The 1-5 judge can't separate the two chunkers; it does show semantic chunks lose nothing while the generator reads about 13,500 characters of context per answer instead of 16,800.

### Judge comparison

The same 50 answers (corpus cleanup run) scored by three judges. Counts are answers per score; no judge gave any answer a 1 or 2.

| Dimension | GPT-4o-mini judge | Gemma, prompt v1 | Gemma, prompt v2 |
|-----------|-------------------|------------------|------------------|
| Contextual alignment | 4.98 (49 × 5) | 5.00 (50 × 5) | 4.98 (49 × 5) |
| Source faithfulness | 4.90 (45 × 5) | 4.98 (49 × 5) | 4.98 (49 × 5) |
| Specificity | 4.90 (45 × 5) | 4.56 (28 × 5) | 4.78 (39 × 5) |
| Bias handling | 4.22 (20 × 5, 9 × 3) | 3.82 (5 × 5, 14 × 3) | 3.80 (5 × 5, 15 × 3) |
| Overall | 4.75 | 4.59 | 4.64 |

Gemma is stricter than GPT-4o-mini on specificity and bias handling, the two dimensions that still separate answers. Prompt v2 describes every score from 1 to 5 instead of only 1 and 5, and adds a rule that answers saying the passages don't cover a question are not penalized. It did not break the ceiling on alignment and faithfulness, and it raised specificity on 11 answers. The likely reason is that GPT-4o-mini's answers are consistently on-topic and sourced, and a 1-5 scale can't separate good answers from better ones. Those two dimensions still catch a collapse, as the Mistral comparison shows.

The Gemma judge is deterministic: a repeat v2 run produced identical scores and reasoning for all 50 answers. Bias handling still changed on 12 of 50 answers between v1 and v2, even though its wording was identical, while its average moved only from 3.82 to 3.80. Rewording one part of the prompt shifts scores on the others, so every prompt version needs its own baseline, which the versioned judge label enforces.

Run-to-run variation in a full evaluation comes from generation, not judging: answers are regenerated at temperature 0.2 on each run. The 0.3 regression threshold has to absorb that variation, which has not yet been measured.

### Model comparison findings

Scored by the GPT-4o-mini judge before the corpus cleanup.

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

- Judge scores are coarse. Alignment and faithfulness score 5 on 49 of 50 GPT-4o-mini answers, so they detect large regressions but not small improvements. Comparing two retrieval setups side by side (pairwise judging) would be more sensitive.
- Judge scores are sensitive to prompt wording: changing the anchors for three dimensions moved bias handling scores on 12 of 50 answers. Scores from different prompt versions are not comparable.
- The variation in scores between two full evaluation runs with no changes, which comes from generation at temperature 0.2, has not been measured, so the 0.3 regression threshold is not yet calibrated.
- Results before the judge switch, including the Mistral comparison, were scored by GPT-4o-mini judging its own answers, which tends to favor them. They are not comparable with Gemma-judged results.
- Corpus coverage of Paiute spiritual and religious practices is sparse. Queries on this topic return insufficient context.
- Transliteration of Paiute language terms varies across corpus documents from different eras. Queries about specific terminology may surface variant spellings depending on which sources are retrieved.
- Ghosts of the Sagebrush is primarily a photo document. Extracted text is fragmentary and retrieved chunks should be treated as partial context only.
- OCR preprocessing is not implemented. All corpus documents must be text-selectable PDFs.
- Mistral 7B inference runs on CPU on AMD hardware without ROCm configuration, producing query latency of approximately 51 seconds per query.

---

## Future Work

- Multimodal ingestion of historical maps and photographs via vision model description pipeline
- Evaluate Anthropic Claude as an alternative generation model for nuanced historical prose synthesis
- Pairwise judging to compare retrieval and chunking changes more sensitively than 1-5 scores
- Rerun the Mistral 7B comparison under the Gemma judge (its answers predate saved answer files, so they must be generated again)
- Expanded owensvalleyhistory.com crawl coverage
- Visualization of evaluation scores across query dimensions and runs
- ROCm configuration for AMD GPU acceleration of local inference