import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from src.retrieve import retrieve
from src.generate import generate
from src.judge import judge, JUDGE_LABEL
from src.config import OUTPUTS_DIR
from src.results import DIMENSIONS

TEST_QUERIES = [
    "What did the Owens Valley Paiute families diet consist of during the winter months?",
    "Describe the landscape of the Owens Valley floor in early spring before the aqueduct was built and the land dried up.",
    "Describe where Owens Valley Paiute families lived after they returned from their forced relocation to Fort Tejon.",
    "How did the LA aqueduct project affect water access for Owens Valley residents?",
    "What role did women's clubs play in California civic life in the early 1900s?",
    "Describe the general geology of Owens Valley.",
    "Describe the eastern Sierra Nevada mountain passes and terrain.",
    "How did Los Angeles justify the acquisition of Owens Valley water rights?",
    "What flora and fauna were native to the Owens Valley region?",
    "How did Paiute communities respond to land dispossession?",
    "What were the environmental consequences of the aqueduct diversion?",
    "How did Owens Valley Paiute families live after settlers took over Owens Valley?",
    "What were some ethical and moral dilemmas created by LA's approach to the aqueduct?",
    "Who were some notable families or people in the creation of settler communities in Owens Valley?",
    "Describe Owens Valley Paiute religion.",
    "What was the name of the train that originally ran through Owens Valley?",
    "What counties did the slim princess run through?",
    "When was the slim princess built?",
    "What kind of train was the slim princess?",
    "How did the Owens Valley locals retaliate against the aqueduct in the years following the finished project?",
    "Describe how the white settlers and native paiutes got along in Owens Valley in the years after the aqueduct was built.",
    "Describe the chemical makeup of Owens Lake before the aqueduct diverted its water.",
    "Was Owens Valley a desert before the aqueduct diverted the water?",
    "Who was William Mulholland and what was his role in the Los Angeles Aqueduct project?",
    "What was the Saint Francis Dam disaster and how did it affect public trust in the Los Angeles Department of Water and Power?",
    "Describe the Paiute people's relationship with water and land in Owens Valley before white settlement.",
    "What was the role of Fred Eaton in acquiring Owens Valley land for the Los Angeles Aqueduct?",
    "How did the construction of the Los Angeles Aqueduct affect agriculture in Owens Valley?",
    "What happened to Owens Lake after the aqueduct diverted its water, and what environmental consequences followed?",
    "Describe the economic conditions of Bishop, California in the decades following the aqueduct completion.",
    "What legal battles did Owens Valley residents pursue against the City of Los Angeles over water rights?",
    "How did the Dust Bowl of Owens Lake affect surrounding communities in terms of air quality and public health?",
    "What role did the Bureau of Reclamation play in Owens Valley water disputes?",
    "Describe the relationship between the City of Los Angeles and Inyo County over water and land ownership.",
    "How did indigenous land use practices in Owens Valley differ from those of white settlers in the late 1800s?",
    "What items did the Owens Valley Paiute primarily manufacture before 1910?",
    "What was the role of the Los Angeles Times in shaping public opinion about the Owens Valley aqueduct project?",
    "Describe the irrigation systems that Owens Valley farmers built before Los Angeles acquired their water rights.",
    "What happened to the town of Keeler, California after Owens Lake dried up?",
    "How did the Second Los Angeles Aqueduct differ from the first in terms of construction and impact?",
    "Describe the role of the Owens Valley in supplying water during Los Angeles's early population boom.",
    "What trade relationships existed between Owens Valley Paiute communities and neighboring tribes?",
    "How did the arrival of the railroad change economic and social life in Owens Valley?",
    "Describe the seasonal migration patterns of Owens Valley Paiute families before white settlement.",
    "What was the significance of pine nuts in Owens Valley Paiute culture and subsistence?",
    "How did Owens Valley ranchers and farmers organize politically to resist Los Angeles water acquisition?",
    "Describe the living conditions at the Fort Tejon reservation during the Paiute forced relocation.",
    "What role did alkali dust from dry Owens Lake play in regional environmental policy debates?",
    "How did the completion of the aqueduct change land values and property ownership patterns in Owens Valley?",
    "Describe the oral traditions or storytelling practices of the Owens Valley Paiute people.",
]

ANSWER_PREVIEW_LENGTH = 1000
CSV_FIELDS = [
    "query",
    "model",
    "judge_model",
    "contextual_alignment",
    "source_faithfulness",
    "specificity",
    "bias_handling",
    "reasoning",
    "sources_used",
    "answer_preview",
]


def safe_name(name: str) -> str:
    return name.replace("/", "_").replace(":", "_")


def get_csv_path(model: str, judge_model: Optional[str] = None) -> Path:
    # Re-scored runs get the judge in the filename so the original CSV is kept
    if judge_model:
        return OUTPUTS_DIR / f"eval_results_{safe_name(model)}__judge_{safe_name(judge_model)}.csv"
    return OUTPUTS_DIR / f"eval_results_{safe_name(model)}.csv"


def get_answers_path(model: str) -> Path:
    return OUTPUTS_DIR / f"eval_answers_{safe_name(model)}.jsonl"


def build_row(query: str, model: str, answer: str, chunks: List[Dict], scores: Dict) -> Dict:
    sources_used = ", ".join(
        set(c["metadata"]["source"] for c in chunks)
    )

    return {
        "query": query,
        "model": model,
        "judge_model": JUDGE_LABEL,
        "contextual_alignment": scores.get("contextual_alignment"),
        "source_faithfulness": scores.get("source_faithfulness"),
        "specificity": scores.get("specificity"),
        "bias_handling": scores.get("bias_handling"),
        "reasoning": scores.get("reasoning", ""),
        "sources_used": sources_used,
        "answer_preview": answer[:ANSWER_PREVIEW_LENGTH].replace("\n", " "),
    }


def build_error_row(query: str, model: str, error: str) -> Dict:
    return {
        "query": query,
        "model": model,
        "judge_model": JUDGE_LABEL,
        "contextual_alignment": None,
        "source_faithfulness": None,
        "specificity": None,
        "bias_handling": None,
        "reasoning": error,
        "sources_used": "",
        "answer_preview": "",
    }


def print_scores(row: Dict) -> None:
    print(f"  Scores — alignment: {row['contextual_alignment']} | "
          f"faithfulness: {row['source_faithfulness']} | "
          f"specificity: {row['specificity']} | "
          f"bias: {row['bias_handling']}")


def run_evaluation(model: str = "openai") -> List[Dict]:
    """
    Runs every test query through retrieve, generate, and judge.
    Full answers and retrieved chunks are written to a JSONL file as each
    query finishes, so a run can be re-scored later with a different judge.
    """
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    answers_path = get_answers_path(model)
    results = []

    with open(answers_path, "w", encoding="utf-8") as answers_file:
        for i, query in enumerate(TEST_QUERIES):
            print(f"\n[{i + 1}/{len(TEST_QUERIES)}] {query}")
            record = {"query": query, "model": model}

            try:
                chunks = retrieve(query, strict=True)
                result = generate(query, chunks, model=model)
                record.update({"answer": result["answer"], "chunks": chunks})

                scores = judge(query, result["answer"], chunks)
                row = build_row(query, model, result["answer"], chunks, scores)
                results.append(row)
                print_scores(row)

            except Exception as e:
                print(f"  [ERROR] Query failed: {e}")
                record["error"] = str(e)
                results.append(build_error_row(query, model, f"Pipeline error: {e}"))

            answers_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            answers_file.flush()

    print(f"\n  Answers saved to {answers_path}")
    return results


def load_answers(answers_path: Path) -> List[Dict]:
    with open(answers_path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def rejudge(answers_path: Path) -> List[Dict]:
    """
    Re-scores saved answers with the current judge model and prompt, without
    retrieving or generating again.
    """
    records = load_answers(answers_path)
    results = []

    for i, record in enumerate(records):
        query = record["query"]
        model = record["model"]
        print(f"\n[{i + 1}/{len(records)}] {query}")

        if "answer" not in record:
            print("  [SKIP] No saved answer for this query.")
            results.append(build_error_row(
                query, model, f"Pipeline error: {record.get('error', 'no saved answer')}"
            ))
            continue

        try:
            scores = judge(query, record["answer"], record["chunks"])
            row = build_row(query, model, record["answer"], record["chunks"], scores)
            results.append(row)
            print_scores(row)
        except Exception as e:
            print(f"  [ERROR] Judge failed: {e}")
            results.append(build_error_row(query, model, f"Judge error: {e}"))

    return results


def save_results(results: List[Dict], csv_path: Path) -> None:
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(results)
    print(f"\n  Results saved to {csv_path}")


def print_summary(results: List[Dict], model: str) -> None:
    print("\n" + "=" * 50)
    print(f"EVALUATION SUMMARY — {model.upper()}")
    print(f"Judge: {JUDGE_LABEL}")
    print("=" * 50)

    dimension_averages = {}
    for dim in DIMENSIONS:
        scores = [r[dim] for r in results if r[dim] is not None]
        if scores:
            avg = round(sum(scores) / len(scores), 2)
            dimension_averages[dim] = avg
            print(f"  {dim:30s} {avg} / 5")
        else:
            dimension_averages[dim] = 0
            print(f"  {dim:30s} N/A")

    valid_averages = [v for v in dimension_averages.values() if v > 0]
    if valid_averages:
        overall = round(sum(valid_averages) / len(valid_averages), 2)
        weakest = min(dimension_averages, key=dimension_averages.get)
        print(f"\n  Overall average:   {overall} / 5")
        print(f"  Weakest dimension: {weakest}")

    print(f"  Queries evaluated: {len(results)}")
    print("=" * 50)


def main() -> None:
    model = "openai"
    rejudge_name = None
    args = sys.argv[1:]

    for i, arg in enumerate(args):
        if arg.startswith("--model="):
            model = arg.split("=", 1)[1]
        elif arg == "--model" and i + 1 < len(args):
            model = args[i + 1]
        elif arg.startswith("--rejudge="):
            rejudge_name = arg.split("=", 1)[1]
        elif arg == "--rejudge" and i + 1 < len(args):
            rejudge_name = args[i + 1]

    if rejudge_name:
        answers_path = OUTPUTS_DIR / rejudge_name
        if not answers_path.exists():
            print(f"  [ERROR] File not found: {answers_path}")
            sys.exit(1)

        print(f"Re-scoring saved answers — {answers_path.name}")
        print(f"Judge: {JUDGE_LABEL}\n")

        results = rejudge(answers_path)
        model = results[0]["model"] if results else model
        save_results(results, get_csv_path(model, JUDGE_LABEL))
        print_summary(results, model)
        return

    print(f"Starting evaluation pipeline — model: {model}")
    print(f"Judge: {JUDGE_LABEL}")
    print(f"Queries to evaluate: {len(TEST_QUERIES)}\n")

    results = run_evaluation(model)
    save_results(results, get_csv_path(model))
    print_summary(results, model)


if __name__ == "__main__":
    main()