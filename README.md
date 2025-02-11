
# Wine Quality Prediction MLOps Project

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)
![Cloud](https://img.shields.io/badge/Cloud-GCP-blue)
![Docker](https://img.shields.io/badge/Docker-container-blue)
![MLOps](https://img.shields.io/badge/MLOps-Complete-green)

## Overview

The **Wine Quality Prediction MLOps Project** is a full-fledged machine learning operations solution that covers the complete lifecycle of a machine learning model—from data ingestion and training to deployment and monitoring. This project was built to help me understand and implement best practices in MLOps using a combination of tools and frameworks.

The application predicts the quality of wine based on its physicochemical properties. It is served via a REST API and deployed as a Docker container on Google Cloud Platform. The project also includes automated pipelines for model training, versioning, infrastructure provisioning, CI/CD, and monitoring.

---

## Table of Contents

- [Features](#features)
- [User Guide](#user-guide)
- [Developer Guide](#developer-guide)
  - [Architecture Overview](#architecture-overview)
  - [Project Structure](#project-structure)
  - [Toolchain & Pipelines](#toolchain--pipelines)
- [Setup & Deployment](#setup--deployment)
  - [Local Development](#local-development)
  - [CI/CD & Cloud Deployment](#cicd--cloud-deployment)
- [Monitoring](#monitoring)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **API for Wine Quality Prediction:**  
  A FastAPI-based REST API that exposes an endpoint `/predict` to receive wine features and return quality predictions.

- **Automated Training Pipeline:**  
  An Airflow DAG orchestrates data ingestion, preprocessing, training, and evaluation of the ML model. Model experiments are tracked using MLflow and versioned with DVC.

- **Infrastructure as Code:**  
  The entire infrastructure (VMs, firewall rules, etc.) is provisioned via Terraform, ensuring reproducibility and ease of management.

- **CI/CD Pipeline:**  
  GitHub Actions pipelines manage code quality (linting and tests), Docker image building, and deployment to GCP.

- **Monitoring & Observability:**  
  The project includes monitoring capabilities using Evidently for model drift detection and Prometheus/Grafana for application metrics.

---

## User Guide

### How to Access the API

Once deployed, the API is accessible via the public IP address of the Compute Engine instance. For example, it is now accessible on the IP `34.79.2.159`, the API endpoint is: http://34.79.2.159/predict

#### Example Request

Send a POST request with a JSON payload containing the wine features:

```bash
curl -X POST http://34.79.2.159/predict \
  -H "Content-Type: application/json" \
  -d '{
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.70,
    "citric_acid": 0.00,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11,
    "total_sulfur_dioxide": 34,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4
  }' 
  ```
  The API will respond with the predicted wine quality.

## Developer Guide

### Architecture Overview

The project is organized into several key components:

-   **API Service:**  
    Built with FastAPI, the service loads a pre-trained ML model for predicting wine quality and exposes REST endpoints.
    
-   **Model Training Pipeline:**  
    An Airflow DAG orchestrates the following steps:
    
    -   **Data Ingestion:** Load the Wine Quality dataset.
    -   **Model Training & Evaluation:** Train a RandomForest model, evaluate performance with RMSE, and track experiments using MLflow.
    -   **Versioning:** DVC is used to track datasets and model artifacts, ensuring reproducibility.
-   **CI/CD & Infrastructure:**
    
    -   **GitHub Actions:** Automates linting, testing, Docker image building, and deployment.
    -   **Terraform:** Manages the provisioning of cloud infrastructure on GCP (Compute Engine instances, firewall rules, etc.).
    -   **Docker:** The API and other components are containerized for consistent deployments.
-   **Monitoring:**  
    The project includes a monitoring pipeline:
    
    -   **Evidently:** Generates HTML reports for model drift and data quality.
    -   **Prometheus & Grafana:** Collect and visualize application metrics (deployed separately via Docker Compose).

### Project Structure

```
wine-quality-prediction/
├── app/                     # API code and model loading logic
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── model.py             # Code to load and use the ML model
├── data/                    # Dataset files (e.g., winequality.csv)
├── terraform/               # Terraform configuration files for GCP
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars
├── tests/                   # Unit tests for the API and model functions
│   ├── test_main.py
│   └── test_model_prediction.py
├── docker-compose.airflow.yml  # (Optional) For deploying Airflow
├── docker-compose.monitoring.yml # (Optional) For deploying Prometheus/Grafana
├── Dockerfile.api           # Dockerfile for building the API image
├── pyproject.toml           # Poetry configuration and dependencies
├── README.md                # This file
└── ...
```

### Toolchain & Pipelines

-   **FastAPI & Uvicorn:** For serving the API.
-   **Airflow:** Orchestrates the training pipeline (data ingestion, preprocessing, training, evaluation).
-   **MLflow:** Tracks model parameters, metrics, and artifacts.
-   **DVC:** Versions data and model files.
-   **Terraform:** Provisions cloud infrastructure on GCP.
-   **GitHub Actions:** Runs tests, builds Docker images, and deploys both the infrastructure and API.
-   **Artifact Registry:** Stores Docker images.
-   **Prometheus/Grafana & Evidently:** Provide monitoring and observability (deployed independently).

## Setup & Deployment

### Local Development

1.  **Clone the Repository:**

```
git clone https://github.com/yourusername/wine-quality-prediction.git
cd wine-quality-prediction
```

2. **Install Dependencies with Poetry:**
```
poetry install
```
3. **Run the API Locally:**
```
uvicorn app.main:app --reload
```
The API will be accessible at `http://127.0.0.1:8000`.

4. **Run Tests:**
```
poetry run pytest
```

### CI/CD & Cloud Deployment

-   **CI/CD Pipelines:**  
    GitHub Actions handles:
    
    -   **Linting & Testing:** Ensuring code quality.
    -   **Docker Image Building:** Creating the container image for the API.
    -   **Terraform Deployment:** Provisioning infrastructure on GCP.
    -   **API Deployment:** SSH into the VM, pulling and running the Docker image.
-   **Infrastructure Provisioning:**  
    Use Terraform (inside GitHub Actions) to deploy:
    
    -   Compute Engine instances
    -   Firewall rules
    -   Other resources as needed
-   **Artifact Registry:**  
    Docker images are pushed to Artifact Registry and then pulled by the VM during deployment.

## Monitoring

-   **Evidently HTML Report:**  
    A monitoring script generates an HTML report detailing data quality and model drift.
    
    -   **Access Option:** You can serve this report via a lightweight HTTP server (e.g., using `python -m http.server`) or host it on a static site (e.g., a GCS bucket with static website hosting).
-   **Prometheus & Grafana:**  
    For real-time monitoring of API metrics, these tools are deployed via separate `docker-compose` files. They provide dashboards for tracking performance, latency, and error rates.

## Final Notes

Working on this project allowed me to put into practice the full spectrum of MLOps—from configuring CI/CD pipelines and managing infrastructure as code with Terraform, to integrating training, versioning, and model monitoring tools into one cohesive system. This project has deepened my understanding of the challenges involved in deploying and operating machine learning tools in production environments. 
