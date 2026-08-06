import os
import sys
from fastapi.testclient import TestClient

# Add project root to python path for safe imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model"] == "loaded"

def test_predict_endpoint_positive():
    response = client.post("/predict", json={"tweet": "I love this new phone, the camera is amazing!"})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "Positive"
    assert "confidence_score" in data
    assert 0.0 <= data["confidence_score"] <= 1.0

def test_predict_endpoint_negative():
    response = client.post("/predict", json={"tweet": "This phone is terrible and customer service is the worst."})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "Negative"
    assert "confidence_score" in data
    assert 0.0 <= data["confidence_score"] <= 1.0

def test_predict_endpoint_empty_value_validation():
    response = client.post("/predict", json={"tweet": ""})
    # Should fail validation (min_length=1) with 422
    assert response.status_code == 422

def test_predict_endpoint_oversized_value_validation():
    # Tweet exceeding 280 characters should fail validation
    long_tweet = "a" * 300
    response = client.post("/predict", json={"tweet": long_tweet})
    assert response.status_code == 422
