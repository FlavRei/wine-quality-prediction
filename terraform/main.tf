terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
}

resource "google_compute_instance" "wine-quality-prediction_instance" {
  name         = "wine-quality-prediction-instance"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata = {
    ssh-keys = "flavian_reignault:${file(var.gcp_ssh_public_key)}"
  }

  tags = ["wine-quality-prediction"]
}

resource "google_compute_firewall" "allow-http" {
  name    = "allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["wine-quality-prediction"]
}

resource "google_compute_firewall" "allow-ssh" {
  name    = "allow-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["wine-quality-prediction"]
}

resource "google_artifact_registry_repository" "wine-quality-prediction-api" {
  location      = "europe-west1"
  repository_id = "wine-quality-prediction-api"
  description   = "Docker repository for wine-quality-prediction API"
  format        = "DOCKER"
}

resource "google_cloud_run_service" "streamlit_app" {
  name     = "wine-quality-streamlit-app"
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

resource "google_cloud_run_service_iam_member" "streamlit_app_noauth" {
  service  = google_cloud_run_service.streamlit_app.name
  location = google_cloud_run_service.streamlit_app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
