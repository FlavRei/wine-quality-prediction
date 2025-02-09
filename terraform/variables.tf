variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west9"
}

variable "zone" {
  description = "GCP area"
  type        = string
  default     = "europe-west9-a"
}

variable "machine_type" {
  description = "Machine type for the instance"
  type        = string
  default     = "e2-micro"
}

variable "credentials_file" {
  description = "GCP Service Account JSON"
  type        = string
}

variable "gcp_ssh_public_key" {
  description = "Path to the GCP SSH public key"
  type        = string
}
