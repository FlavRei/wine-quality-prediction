from app.model_prediction import load_model, predict
import os

RED_WINE_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..\\app\\model\\red_wine_model.pkl')

def test_load_model():
    model = load_model(RED_WINE_MODEL_PATH)
    assert model is not None

def test_predict():
    input_data = {
        "fixed acidity": 7.0,
        "volatile acidity": 0.5,
        "citric acid": 0.3,
        "residual sugar": 1.5,
        "chlorides": 0.05,
        "free sulfur dioxide": 15.0,
        "total sulfur dioxide": 30.0,
        "density": 0.995,
        "pH": 3.2,
        "sulphates": 0.6,
        "alcohol": 10.0
    }
    prediction = predict(input_data)
    assert isinstance(prediction, float)
