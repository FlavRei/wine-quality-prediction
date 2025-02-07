from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert "message" in json_data
    assert "Welcome" in json_data["message"]

def test_predict_endpoint():
    payload = {
        "fixed_acidity": 7.0,
        "volatile_acidity": 0.5,
        "citric_acid": 0.3,
        "residual_sugar": 1.5,
        "chlorides": 0.05,
        "free_sulfur_dioxide": 15.0,
        "total_sulfur_dioxide": 30.0,
        "density": 0.995,
        "pH": 3.2,
        "sulphates": 0.6,
        "alcohol": 10.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "predicted_quality" in json_data, "The response must contain the key 'predicted_quality'"
