# UV Python Setup (Windows)

> Fast Python package manager. Always use UV for Python projects.

## New Project Setup

```powershell
# Create project folder
mkdir my-project
cd my-project

# Initialize project
uv init

# Create virtual environment
uv venv

# Activate virtual environment
.venv\Scripts\Activate.ps1
```

## Package Management

```powershell
# Install packages
uv add fastapi
uv add "fastapi[standard]"
uv add fastapi sqlalchemy pydantic

# Install dev dependency
uv add --dev pytest

# Remove package
uv remove fastapi

# Sync all dependencies
uv sync
```

## Clone Existing Project

```powershell
git clone <repo-url>
cd project-name

# Create venv and install all deps
uv venv
uv sync

# Activate
.venv\Scripts\Activate.ps1
```

## Run Commands

```powershell
# Run Python script
uv run python main.py

# Run FastAPI dev server
uv run fastapi dev main.py

# Run tests
uv run pytest
```

## Python Version

```powershell
# Install Python version
uv python install 3.11

# Use specific version
uv venv --python 3.11
```

## Quick Reference

| Action | Command |
|--------|---------|
| Create venv | `uv venv` |
| Activate venv | `.venv\Scripts\Activate.ps1` |
| Add package | `uv add <package>` |
| Add dev package | `uv add --dev <package>` |
| Sync deps | `uv sync` |
| Run script | `uv run python <file>` |

## .gitignore

```gitignore
.venv/
__pycache__/
.env
```

## Rules

- ✅ Always create venv with `uv venv`
- ✅ Always activate before running Python
- ✅ Use `uv add` to track dependencies
- ✅ Commit `uv.lock` and `pyproject.toml`
- ❌ Never commit `.venv/`
