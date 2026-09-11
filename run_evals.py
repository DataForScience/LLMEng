"""Regression gate for the Banking77 triage prompt. Wire this into CI.

Usage:
    python run_evals.py --model gpt-4.1-mini --min-queue-accuracy 0.85 --min-intent-accuracy 0.60
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel


def main():
    parser = argparse.ArgumentParser(description="LLM regression gate")
    parser.add_argument("--model", default="gpt-4.1-mini")
    parser.add_argument("--dataset", default="data/golden_banking77.jsonl")
    parser.add_argument("--taxonomy", default="data/banking77_taxonomy.json")
    parser.add_argument("--prompt", default="prompts/triage_v1.0.0.json")
    parser.add_argument("--min-queue-accuracy", type=float, default=0.85)
    parser.add_argument("--min-intent-accuracy", type=float, default=0.60)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    taxonomy = json.loads(Path(args.taxonomy).read_text())
    prompt = json.loads(Path(args.prompt).read_text())
    golden = [json.loads(line) for line in Path(args.dataset).read_text().splitlines()]
    intents = ", ".join(taxonomy["intents"])
    client = OpenAI()

    class Triage(BaseModel):
        queue: Literal[tuple(taxonomy["queues"])]
        intent: Literal[tuple(taxonomy["intents"])]
        summary: str
        requires_human: bool

    def score(row):
        response = client.chat.completions.parse(
            model=args.model,
            messages=[{"role": "system", "content": prompt["system"]},
                      {"role": "user", "content": prompt["user_template"].format(text=row["text"], intents=intents)}],
            response_format=Triage,
            temperature=0,
        )
        prediction = response.choices[0].message.parsed
        return prediction.queue == row["queue"], prediction.intent == row["intent"]

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(score, golden))

    queue_accuracy = sum(q for q, _ in results) / len(results)
    intent_accuracy = sum(i for _, i in results) / len(results)
    print(f"queue accuracy:  {queue_accuracy:.3f} (threshold {args.min_queue_accuracy})")
    print(f"intent accuracy: {intent_accuracy:.3f} (threshold {args.min_intent_accuracy})")
    print(f"n = {len(results)}  model = {args.model}  prompt = {prompt['version']}")

    if queue_accuracy < args.min_queue_accuracy or intent_accuracy < args.min_intent_accuracy:
        print("FAIL: below threshold. Blocking the deploy.")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
