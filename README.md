# URL to Blog Converter

A FastAPI project that converts web content into blog posts.

## Setup

This project uses `uv` for dependency management.

1.  **Install uv** (if not already installed).
2.  **Initialize the environment**:
    ```powershell
    uv sync
    ```

## Running the App

To run the development server:

```powershell
uv run fastapi dev app/main.py
```

## Features (Planned)

- URL Crawling with `crawl4ai`.
- AI-powered blog generation using `pydantic-ai`.
