"""Your minimal agent harness. Target: under 300 lines including tools.py.

The loop: assemble context -> call model -> dispatch tools (with permission checks) -> append results -> stop or loop.
Run `pytest -q` to see what is still missing. Run against your local model with:
    python -m mini_harness.harness "How many Python files are in this repo?"
"""

from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field

from .tools import TOOLS, ToolError  # noqa: F401

SYSTEM = (
    "You are a coding agent working in a repository. Use tools to look before you answer. "
    'To call a tool reply with JSON only: {"tool": "<name>", "args": {...}}. '
    'When you are finished reply with JSON: {"final": "<your answer>"}. '
)


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


@dataclass
class Budget:
    max_turns: int = 12
    max_tokens: int = 20_000
    turns: int = 0
    tokens: int = 0

    def exhausted(self) -> str | None:
        """TODO: return a reason string when either limit is reached, else None."""
        return None


@dataclass
class Result:
    answer: str | None
    stop_reason: str
    transcript: list[dict] = field(default_factory=list)
    tokens: int = 0
    turns: int = 0


class OpenAICompatibleModel:
    """Calls any OpenAI-compatible chat endpoint. Set MODEL_BASE_URL and MODEL_NAME for your local model server."""

    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or os.environ.get("MODEL_BASE_URL", "http://localhost:11434/v1")).rstrip("/")
        self.model = model or os.environ.get("MODEL_NAME", "qwen2.5-coder:7b")

    def __call__(self, messages: list[dict]) -> str:
        body = json.dumps({"model": self.model, "messages": messages, "temperature": 0}).encode()
        req = urllib.request.Request(
            self.base_url + "/chat/completions", data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:  # noqa: S310
            return json.load(resp)["choices"][0]["message"]["content"]


def parse_reply(text: str) -> dict:
    """TODO: models wrap JSON in prose and code fences. Find the first JSON object; if none, treat it as final."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"final": text}


class Harness:
    def __init__(self, model, root, budget: Budget | None = None, approve=None):
        self.model = model
        self.root = os.path.abspath(root)
        self.budget = budget or Budget()
        self.approve = approve or (lambda name, args: False)  # the permission gate

    def assemble(self, task: str) -> list[dict]:
        """TODO: build the first messages: system prompt + tool list + AGENTS.md (if present) + the task."""
        return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]

    def dispatch(self, call: dict) -> str:
        """TODO: look up the tool, check its arguments, ask approve() if needs_approval, run it,
        turn ToolError into a message, and truncate long output. Never let an exception escape."""
        tool = TOOLS[call["tool"]]
        return tool.run(self.root, **call.get("args", {}))

    def run(self, task: str) -> Result:
        """TODO: the loop. Check the budget before every model call, count turns and tokens,
        stop on a final answer, otherwise dispatch and append the result. Pass the model a copy of the messages."""
        messages = self.assemble(task)
        reply = self.model(messages)
        parsed = parse_reply(reply)
        return Result(parsed.get("final"), "final answer", messages)


if __name__ == "__main__":
    import sys

    task = " ".join(sys.argv[1:]) or "How many Python files are in this repository? Use the tools."
    res = Harness(OpenAICompatibleModel(), ".").run(task)
    print(f"\n[{res.stop_reason}; {res.turns} turns; ~{res.tokens} tokens]\n{res.answer}")
