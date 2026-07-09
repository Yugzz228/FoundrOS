# 1. Python and Modern Tooling

Date: 2026-07-09

## Status
Accepted

## Context
FoundrOS needs a robust, scalable backend language to orchestrate multiple AI agents. The Python ecosystem is the undisputed leader in AI, but standard Python dependency management (`pip` + `requirements.txt`) can become brittle over time.

## Decision
We will use:
- **Python 3.12** for the latest language features.
- **uv** as the package manager for speed and reliability.
- **pyproject.toml** for dependency management.
- **Ruff** for fast linting and formatting.
- **pytest** for testing.

## Consequences
- We gain modern, fast tooling and eliminate the need for `requirements.txt`.
- Onboarding requires developers to install `uv` and understand `pyproject.toml`.
