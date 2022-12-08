variable "SECRET_KEY" {
  description = "Required secret key"
  type        = string
  sensitive   = "true"
}

variable "MONGO_DATABASE_NAME" {
  description = "Name of the database"
  type        = string
  sensitive   = "false"
}

variable "GITHUB_CLIENT_ID" {
  description = "client id"
  type        = string
  sensitive   = "true"
}

variable "GITHUB_CLIENT_SECRET" {
  description = "client secret value"
  type        = string
  sensitive   = "true"
}

variable "ACCOUNT_KEY" {
  description = "Storage account key"
  type        = string
  sensitive   = "true"
}



