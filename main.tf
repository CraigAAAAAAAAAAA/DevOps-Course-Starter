# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "LV21_CraigBeasley_ProjectExercise"
    storage_account_name = "m12craigbeasley"
    container_name       = "mod12container"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}
data "azurerm_resource_group" "main" {
  name = "LV21_CraigBeasley_ProjectExercise"
}

#Create the resource group

resource "azurerm_app_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

# Create the App Service

resource "azurerm_app_service" "main" {
  name                = "module12-todo"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id

  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|craigbeasley/todo_app:prod"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGO_CONNECTION_STRING"    = azurerm_cosmosdb_account.main.connection_strings[0]
    "SECRET_KEY"                 = var.SECRET_KEY
    "GITHUB_CLIENT_SECRET"       = var.GITHUB_CLIENT_SECRET
    "GITHUB_CLIENT_ID"           = var.GITHUB_CLIENT_ID
    "MONGO_DATABASE_NAME"        = var.MONGO_DATABASE_NAME
  }
}

# Create the MongoDB Resource

resource "azurerm_cosmosdb_account" "main" {
  name                = "module12testdb"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  consistency_policy {
    consistency_level = "Session"
  }

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  lifecycle {
    prevent_destroy = "true"
  }

  mongo_server_version = "3.6"

  enable_automatic_failover = true

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "mongodb" {
  name                = "module12exercise"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
}

