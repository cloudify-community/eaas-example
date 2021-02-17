terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "2.47.0"
    }
  }
}

provider "azurerm" {
  features {}
}


variable "resource_prefix" {
  type = string
  description = ""
}

variable "resource_group" {
  type = string
  description = ""
}

variable "azure_location" {
  type = string
  description = ""
}

variable "network_id" {
  type = string
  description = ""
}

variable "private_subnet_id_0" {
  type = string
  description = ""
}

variable "private_subnet_id_1" {
  type = string
  description = ""
}

variable "db_name" {
  type = string
  description = ""
}

variable "master_username" {
  type = string
  description = ""
}

variable "master_user_password" {
  type = string
  description = ""
}


# resource "azurerm_resource_group" "rg" {
#     name     = "${var.resource_group}"
#     location = "${var.azure_location}"
# }

resource "azurerm_postgresql_server" "postgresql-server" {
  name                = format("%s%s", var.db_name, "-server")
  location            = "${var.azure_location}"
  resource_group_name = "${var.resource_group}"

  administrator_login          = "${var.master_username}"
  administrator_login_password = "${var.master_user_password}"

  sku_name                      = "B_Gen5_1"
  version                       = "11"
  storage_mb                    = "5120"
  auto_grow_enabled             = true
  public_network_access_enabled = false
}

resource "azurerm_postgresql_database" "postgresql-db" {
  name                = "${var.db_name}"
  resource_group_name = "${var.resource_group}"
  server_name         = azurerm_postgresql_server.postgresql-server.name
  charset             = "utf8"
  collation           = "English_United States.1252"
}

resource "azurerm_postgresql_firewall_rule" "postgresql-fw-rule" {
  name                = format("%s%s", var.db_name, "-firewall-rule")
  resource_group_name = "${var.resource_group}"
  server_name         = azurerm_mysql_server.postgresql-server.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

output "postgresql_server_fqdn" {
  value = azurerm_postgresql_server.postgresql-server.fqdn
}

# resource "azurerm_sql_server" "sql-server" {
#     name                         = format("%s%s", var.db_name, "-server")
#     resource_group_name          = "${var.resource_group}"
#     location                     = "${var.azure_location}"
#     version                      = "12.0"
#     administrator_login          = "${var.master_username}"
#     administrator_login_password = "${var.master_user_password}"
# }

# resource "azurerm_sql_firewall_rule" "firewall" {
#   name                = "AlllowAzureServices"
#   resource_group_name = "${var.resource_group}"
#   server_name         = "${azurerm_sql_server.sql-server.name}"
#   start_ip_address    = "0.0.0.0"
#   end_ip_address      = "0.0.0.0"
# }

# resource "azurerm_sql_database" "db" {
#   name                             = "${var.db_name}"
#   resource_group_name              = "${var.resource_group}"
#   location                         = "${var.azure_location}"
#   server_name                      = "${azurerm_sql_server.sql-server.name}"
#   edition                          = "Standard"
#   requested_service_objective_name = "S1"
# }

# resource "azurerm_private_endpoint" "db-endpoint" {
#   depends_on          = [azurerm_sql_server.sql-server]
#   name                = format("%s%s", var.db_name, "-endpoint")
#   resource_group_name = "${var.resource_group}"
#   location            = "${var.azure_location}"
#   subnet_id           = "${private_subnet_id_0}"
#   private_service_connection {
#     name                           = "sql-db-endpoint"
#     is_manual_connection           = "false"
#     private_connection_resource_id = azurerm_sql_server.sql-server.id
#     subresource_names              = ["sqlServer"]
#   }
# }
