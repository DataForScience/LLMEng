"""Prompt regression suite. Runs in CI on every change under prompts/."""
import os

import pytest

requires_key = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"), reason="needs an API key"
)

CASES = [
    ("Someone used my card in a shop I have never been to.", "security", True),
    ("How long does a transfer to another bank take?", "transfers", False),
    ("Please close my account, I no longer need it.", "account", True),
    ("My top up by card failed twice today.", "top_up", False),
    ("I was charged twice for the same coffee.", "payments", False),
]

@requires_key
@pytest.mark.parametrize("text,queue,requires_human", CASES)
def test_triage(text, queue, requires_human):
    from triage import triage  # your packaged version of this notebook

    result = triage(text)
    assert result.queue == queue
    assert result.requires_human == requires_human
