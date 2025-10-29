## AI Code Review Assistant Bot

Automated multi-agent LLM-powered code review system integrating GPT‑4, LangChain, Agno, Ollama, and Streamlit for explainable static analysis and CI/CD automation.

## Run locally
1. docker-compose up --build
2. Visit backend: http://localhost:8000
3. Visit dashboard: http://localhost:8501

## GitHub CI/CD Integration
- The `.github/workflows/code-review.yml` triggers run_code_review.py
- The script fetches PR diffs, runs analysis using GPT-4 or Ollama, and posts results directly to GitHub.
