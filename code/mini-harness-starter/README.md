# Mini harness (week 2)

Build the loop every coding agent runs, in under 300 lines, so nothing in the rest of the course is magic.

```bash
python -m pip install -e ".[dev]"
pytest -q                     # 11 tests; most fail until you finish the TODOs
python -m mini_harness.harness "How many Python files are in this repository?"   # against your local model
```

**Where it goes:** copy `mini_harness/` and `tests/` into your `<handle>-labs` repo under `mini-harness/`,
or create a repo from this template. Assignment A2 requires the GitHub Actions run to be green.

**Rules:** write it yourself; an agent may review your code but not write the loop. Do not edit `tests/test_harness.py`;
add your own tests in `tests/test_mine.py`. Make it fail on purpose once, and write up what happened.

**Local model:** any OpenAI-compatible server works (set `MODEL_BASE_URL` and `MODEL_NAME`). No API key or internet
is needed, and the tests use a scripted fake model so they run offline and in CI.
