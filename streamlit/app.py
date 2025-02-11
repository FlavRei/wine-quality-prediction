import streamlit as st
import requests

st.title("Wine quality prediction")
st.write("Choose the characteristics of the wine:")

fixed_acidity = st.slider("Acidité fixe", min_value=4.0, max_value=15.0, value=7.4, step=0.1)
volatile_acidity = st.slider("Acidité volatile", min_value=0.0, max_value=2.0, value=0.7, step=0.01)
citric_acid = st.slider("Acide citrique", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
residual_sugar = st.slider("Sucre résiduel", min_value=0.0, max_value=20.0, value=1.9, step=0.1)
chlorides = st.slider("Chlorures", min_value=0.0, max_value=0.2, value=0.076, step=0.001, format="%.3f")
free_sulfur_dioxide = st.slider("Dioxyde de soufre libre", min_value=1, max_value=100, value=11, step=1)
total_sulfur_dioxide = st.slider("Dioxyde de soufre total", min_value=6, max_value=300, value=34, step=1)
density = st.slider("Densité", min_value=0.990, max_value=1.005, value=0.9978, step=0.0001, format="%.4f")
pH = st.slider("pH", min_value=2.8, max_value=4.0, value=3.51, step=0.01)
sulphates = st.slider("Sulfates", min_value=0.0, max_value=2.0, value=0.56, step=0.01)
alcohol = st.slider("Alcool", min_value=8.0, max_value=15.0, value=9.4, step=0.1)

if st.button("Predict quality"):
    payload = {
        "fixed_acidity": fixed_acidity,
        "volatile_acidity": volatile_acidity,
        "citric_acid": citric_acid,
        "residual_sugar": residual_sugar,
        "chlorides": chlorides,
        "free_sulfur_dioxide": free_sulfur_dioxide,
        "total_sulfur_dioxide": total_sulfur_dioxide,
        "density": density,
        "pH": pH,
        "sulphates": sulphates,
        "alcohol": alcohol
    }

    api_url = "http://34.79.2.159/predict"

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        st.success(f"The predicted quality is: {result.get('predicted_quality')}")
    except Exception as e:
        st.error(f"Error calling the API: {e}")
