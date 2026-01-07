#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install uv for faster dependency resolution
pip install uv

# Install Python dependencies using uv (much faster than pip)
uv pip install --system -r requirements.txt

# Install Playwright browsers (Required by crawl4ai on Linux)
python -m playwright install --with-deps chromium
