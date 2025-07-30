# Vibe Automation SDK

## Development Setup

### Prerequisites
- Python >=3.13
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

### Running Examples

```bash
uv run python examples/form.py
```
