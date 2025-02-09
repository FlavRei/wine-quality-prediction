variable "project_id" {
  description = "L'ID du projet GCP"
  type        = string
}

variable "region" {
  description = "La région GCP"
  type        = string
  default     = "europe-west9"
}

variable "zone" {
  description = "La zone GCP"
  type        = string
  default     = "europe-west9-a"
}

variable "machine_type" {
  description = "Le type de machine pour l'instance"
  type        = string
  default     = "e2-micro"
}

variable "credentials_file" {
  description = "Chemin vers le fichier de clé JSON du compte de service"
  type        = string
}
