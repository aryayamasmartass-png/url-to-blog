#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (Required by crawl4ai on Linux)
python -m playwright install --with-deps chromium
