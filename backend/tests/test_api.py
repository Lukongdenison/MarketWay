from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to MarketWay Navigator API"

def test_search_product():
    # Test searching for a known product
    response = client.get("/product/search?q=shoes")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) > 0
    assert "Blessed Line" in [r["line_name"] for r in data["results"]]

def test_get_line_info():
    response = client.get("/line/info/Mothers Line")
    assert response.status_code == 200
    data = response.json()
    assert data["line_name"] == "Mothers Line"
    assert "medicine" in data["items_sold"]

def test_navigate():
    response = client.get("/navigate?line_name=Mothers Line")
    assert response.status_code == 200
    data = response.json()
    assert "Mothers Line" in data["directions"]
    assert "left" in data["directions"]

def test_history():
    response = client.get("/history")
    assert response.status_code == 200
    # Should return empty or error message if PDF missing, but status 200
    assert "history" in response.json()

# Note: Voice and Image tests require file uploads and are harder to mock simply here without sample files.
# They are skipped for this basic verification.
