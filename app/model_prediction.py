import joblib
import os

RED_WINE_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/red_wine_model.pkl')

def load_model(model):
    if not os.path.exists(model):
        raise FileNotFoundError(f"The model was not found at the location {model}")
    model = joblib.load(model)
    return model

def predict(input_data):
    """
    input_data must be a dictionary with the same keys as the model features.
    Example: {"fixed acidity": 7.4, "volatile acidity": 0.70, ...}
    """
    model = load_model(RED_WINE_MODEL_PATH)
    features = [value for key, value in input_data.items()]
    prediction = model.predict([features])
    return prediction[0]
