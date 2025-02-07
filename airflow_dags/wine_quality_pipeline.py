from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def ingest_data(**kwargs):
    """
    Load the dataset from the data folder and save it as JSON via XCom.
    """
    data_path = os.path.join("/opt/airflow", 'data', 'red_wine_quality.csv')
    df = pd.read_csv(data_path, sep=';')
    kwargs['ti'].xcom_push(key='raw_data', value=df.to_json())
    print("Data ingested.")


def train_model(**kwargs):
    """
    Trains a RandomForest model, saves it and data information in MLflow.
    """
    ti = kwargs['ti']
    raw_data_json = ti.xcom_pull(key='raw_data')
    df = pd.read_json(raw_data_json)

    X = df.drop('quality', axis=1)
    y = df['quality']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    model_path = os.path.join("/opt/airflow", 'app/model', 'red_wine_model.pkl')
    joblib.dump(model, model_path)

    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("WineQuality")
    with mlflow.start_run():
        mlflow.log_param("n_estimators", 100)
        predictions = model.predict(X_test)
        rmse = mean_squared_error(y_test, predictions, squared=False)
        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(model, "model")

    ti.xcom_push(key='model_rmse', value=rmse)
    print(f"Model trained with RMSE = {rmse} and saved in {model_path}.")


def evaluate_model(**kwargs):
    """
    Shows the model metric.
    """
    ti = kwargs['ti']
    rmse = ti.xcom_pull(key='model_rmse')
    print(f"Model evaluation: RMSE = {rmse}")


with DAG(
    'wine_quality_pipeline',
    default_args=default_args,
    description='Pipeline for wine quality prediction',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    data_ingestion = PythonOperator(
        task_id='ingest_data',
        python_callable=ingest_data,
        provide_context=True
    )

    model_training = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        provide_context=True
    )

    model_evaluation = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
        provide_context=True
    )

    data_ingestion >> model_training >> model_evaluation
