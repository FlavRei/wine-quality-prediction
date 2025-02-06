from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.model_prediction import predict

app = FastAPI(
    title="Wine Quality Prediction API",
    description="API to predict wine quality based on its characteristics.",
    version="1.0.0"
)

class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Wine Quality Prediction API!"}

@app.post("/predict")
def predict_wine(features: WineFeatures):
    try:
        input_data = {
            "fixed acidity": features.fixed_acidity,
            "volatile acidity": features.volatile_acidity,
            "citric acid": features.citric_acid,
            "residual sugar": features.residual_sugar,
            "chlorides": features.chlorides,
            "free sulfur dioxide": features.free_sulfur_dioxide,
            "total sulfur dioxide": features.total_sulfur_dioxide,
            "density": features.density,
            "pH": features.pH,
            "sulphates": features.sulphates,
            "alcohol": features.alcohol
        }
        quality = predict(input_data)
        return {"predicted_quality": quality}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
