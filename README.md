# LLM Engineering Masterclass: Production Evals, RAG, Agents & LLMOps

![GitHub](https://img.shields.io/github/license/DataForScience/LLMEng)
[![Twitter @data4sci](https://img.shields.io/twitter/follow/data4sci)](https://twitter.com/intent/follow?screen_name=data4sci)
![GitHub top language](https://img.shields.io/github/languages/top/DataForScience/LLMEng)
![GitHub repo size](https://img.shields.io/github/repo-size/DataForScience/LLMEng)
![GitHub last commit](https://img.shields.io/github/last-commit/DataForScience/LLMEng)

[![Data For Science](https://img.shields.io/badge/Data_For_Science-Subscribe-blue)](https://data4sci.substack.com/)
[![Data Science Briefing](https://img.shields.io/badge/Data_Science_Briefing-Subscribe-blue)](https://data4sci.com/newsletter)

### Code and slides to accompany the live LLM Engineering masterclass by Data For Science, hosted by Packt Publishing.

A prompt edit ships on Friday. Quality drops all week. No test failed because no test exists.

This masterclass teaches engineers to ship LLM systems that survive production: prompts treated as versioned, regression-tested software; an evaluation harness that turns opinions into numbers; model comparisons with confidence intervals and a cost column; retrieval you can measure; agents that validate, gate, retry and degrade on purpose; and an operations layer with tracing, caching, deadlines and a CI regression gate.

Every notebook works on the same real dataset: [Banking77](https://arxiv.org/abs/2003.04807) (Casanueva et al., 2020, CC BY 4.0), 13,083 customer messages to an online bank labeled with one of 77 intents. The whole day of API calls costs a few dollars.

## Setup

Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies and launch Jupyter:

```bash
uv sync
uv run jupyter notebook
```

The notebooks call real model APIs. Export your keys before starting Jupyter:

```bash
export OPENAI_API_KEY=...       # required
export ANTHROPIC_API_KEY=...    # optional, used for the LLM judge in notebook 2
```

Banking77 is downloaded from the [PolyAI GitHub repository](https://github.com/PolyAI-LDN/task-specific-datasets) the first time notebook 1 runs and cached under `data/`.

## Schedule

| # | Notebook | What you build |
|---|----------|----------------|
| 1 | [Prompts as Code](1.%20Prompts%20as%20Code.ipynb) | Banking77 EDA, a six-queue taxonomy, prompts as versioned JSON files, Pydantic-validated outputs with a repair loop, and a five-case regression suite that catches a "harmless" prompt edit |
| 2 | [The Evaluation Harness](2.%20The%20Evaluation%20Harness.ipynb) | A seeded golden set, a parallel runner, deterministic scorers at queue and intent level, an LLM-as-judge with binary criteria, and one saved report per run |
| 3 | [Model Comparison](3.%20Model%20Comparison.ipynb) | A bakeoff between two models with bootstrap confidence intervals, a paired difference, McNemar's exact test, CI width vs. golden set size, and a decision table with cost and latency |
| 4 | [Evaluated RAG](4.%20Evaluated%20RAG.ipynb) | A generated help-center knowledge base, chunking, a numpy vector store, recall@k and MRR, LLM reranking, grounded generation with citations, and when not to use RAG |
| 5 | [Agents and Guardrails](5.%20Agents%20and%20Guardrails.ipynb) | A tool-using agent over a mock bank: Pydantic tool contracts, a dispatcher that returns errors as data, a refund policy gate in code, step budgets, retries and failure injection |
| 6 | [LLMOps](6.%20LLMOps.ipynb) | A JSONL flight recorder for every call, cost and latency percentiles, exact-match caching, deadlines with a fallback model, streaming, and a CLI regression gate wired into GitHub Actions |

## Repository layout

```
.
├── 1. Prompts as Code.ipynb ... 6. LLMOps.ipynb   The six notebooks, in order
├── slides/                    Slide deck (Keynote and PDF)
├── data/
│   ├── banking77_*_raw.csv    Banking77 as downloaded
│   ├── banking77_train.csv    Cleaned splits with intent, queue and requires_human
│   ├── banking77_test.csv
│   ├── banking77_taxonomy.json  Queues, intents and the intent-to-queue map
│   ├── golden_banking77.jsonl   Golden set: one test message per intent (77 rows)
│   └── banking77_kb.jsonl       Generated help-center articles, one per intent
├── prompts/                   Versioned prompts: triage_v1.0.0.json, triage_v2.0.0.json
├── tests/test_triage_prompt.py  Prompt regression suite (pytest)
├── run_evals.py               CLI regression gate with thresholds and an exit code
├── evals.yml                  GitHub Actions workflow that runs the gate on prompt changes
├── output/                    Eval reports, traces and figures written by the notebooks
└── d4sci.mplstyle             Matplotlib style used for all figures
```

## The regression gate

Notebook 6 turns the evaluation harness into a command line tool. Run it locally or in CI:

```bash
uv run python run_evals.py --model gpt-4.1-mini --min-queue-accuracy 0.85 --min-intent-accuracy 0.60
```

It exits non-zero when routing or intent accuracy on the golden set falls below the thresholds. Drop `evals.yml` into `.github/workflows/` to block pull requests that touch `prompts/`, the golden set, the taxonomy or the harness itself.

## Author

<table border="0">
 <tr>
	<td>
	  <img src="data/bgoncalves.png" alt="Bruno Gonçalves" width="150" height="150" style="border-radius: 50%; object-fit: cover;">
	</td>
	<td>
	  <h2>Bruno Gonçalves</h2>
	  <h3>Data For Science, Inc.</h3>
	  <p>
			Web: <a href="http://www.data4sci.com/">www.data4sci.com</a><br>
			Twitter/X: <a href="https://twitter.com/bgoncalves">@bgoncalves</a><br>
			LinkedIn: <a href="https://www.linkedin.com/in/bmtgoncalves/">@bmtgoncalves</a><br>
			Email: <a href="info@data4sci.com">info@data4sci.com</a><br>
			Schedule a Call: <a href="https://data4sci.com/call">https://data4sci.com/call</a>
	  </p>
	</td>
 </tr>
</table>
