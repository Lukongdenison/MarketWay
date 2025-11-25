# Day 2 — Environment Setup Prompt (Send this to Claude)

**PROMPT TO CLAUDE (Day 2):**

> “Today, set up the full development environment for MarketWay.
>
> **Tasks:**
> 1. **Set up Python environment**
>    - Create a virtual environment (e.g., `python -m venv venv`)
>    - Activate it and upgrade `pip`
>    - Install required packages (`fastapi`, `uvicorn`, `pydantic`, `numpy`, `scikit-learn`, `sentence-transformers`, `torch`, `faster-whisper` etc.)
> 2. **Install AI models**
>    - `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
>    - Whisper Base or Small (via `faster-whisper` or `whisper`)
> 3. **Create folder structure**
>    ```
>    /backend
>    /frontend
>    /models
>    /routes
>    /database
>    /utils
>    ```
> 4. **Create the initial backend API structure**
>    - `POST /search`
>    - `POST /voice-search`
>    - `GET /map/vendors`
>    - `GET /navigate?from=&to=`
> 5. **Prepare integration instructions**
>    - How to load MiniLM embeddings and perform semantic search
>    - How to load Whisper model and convert audio to text
>
> **Deliverable:** A concise, step‑by‑step guide (Markdown) that can be copied into a terminal or README to reproduce the environment.
