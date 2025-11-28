# MarketWay Navigator API

Backend service for the MarketWay Navigator, built with FastAPI.

## Folder Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── api.py          # API Endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py       # Configuration
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_loader.py  # Loads JSON/PDF
│   │   ├── image_service.py # Image Recognition
│   │   ├── navigation_service.py # Navigation Logic
│   │   ├── search_service.py # Tavily Search
│   │   └── voice_service.py # STT/TTS
│   ├── __init__.py
│   └── main.py             # Entry Point
├── data/                   # Data Directory
│   ├── images/             # Line Images
│   ├── marketway.json      # Market Data
│   └── Bamenda_Main_Market_History.pdf # History (Optional)
├── tests/
│   └── test_api.py         # Tests
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Setup & Installation

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**:
    Create a `.env` file in `backend/` (or set them in your environment/Render dashboard):
    ```
    TAVILY_API_KEY=your_tavily_api_key_here
    ```

## Running Locally

Start the server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Visit `http://127.0.0.1:8000/docs` to see the interactive Swagger UI documentation. You can test all endpoints directly from there.

## Testing

Run the tests using `pytest`:

```bash
pytest
```

## Deployment on Render

1.  **Create a new Web Service** on Render.
2.  **Connect your repository**.
3.  **Settings**:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
4.  **Environment Variables**: Add `TAVILY_API_KEY`.
5.  **Note on Libraries**:
    *   `tensorflow-cpu` is used for image recognition. If the slug size is too large for Render's free tier, consider switching to a lighter model or removing `tensorflow` from requirements and relying on the fallback logic.
    *   Ensure `backend/data` is included in your repo or mounted as a disk if you want persistence (though for this read-only data, repo is fine).
