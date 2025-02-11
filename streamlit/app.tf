variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

resource "google_cloud_run_service" "wine-quality-prediction-app" {
  name     = "wine-quality-prediction-app"
  location = var.region

  template {
    spec {
      containers {
        image = "europe-west1-docker.pkg.dev/${var.project_id}/wine-quality-prediction-app/wine-quality-prediction-app:latest"
        ports {
          container_port = 8501
        }
      }
    }
  }

  traffic {
    latest_revision = true
    percent         = 100
  }
}

resource "google_cloud_run_service_iam_member" "wine-quality-prediction-app_noauth" {
  service  = google_cloud_run_service.wine-quality-prediction-app.name
  location = google_cloud_run_service.wine-quality-prediction-app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
