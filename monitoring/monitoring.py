import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
import joblib
import json


def load_production_data():
    """
    Simulate data recovery in production here.
    For example, this could come from a database or a log file.
    For this example, we will reuse the training dataset.
    """
    return pd.read_csv("data/red_wine_quality.csv", sep=";")


def load_training_data():
    """
    Load the training dataset that was used to train the model.
    """
    return pd.read_csv("data/red_wine_quality.csv", sep=";")


def generate_drift_report():
    train_data = load_training_data()
    prod_data = load_production_data()

    report = Report(metrics=[
        DataDriftPreset(), 
        DataQualityPreset()
    ])
    report.run(reference_data=train_data, current_data=prod_data)

    report.save_html("monitoring_report.html")
    print("The monitoring report has been generated : monitoring_report.html")


if __name__ == "__main__":
    generate_drift_report()
