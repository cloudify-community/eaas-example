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


variable "azure_location_name" {
  type = string
  description = "Azure location to create resources in"
}

variable "rg_name" {
  type = string
  description = "Resource group name"
}

variable "rg_tags" {
  type = map(string)
  description = "Resource group tags"
}

variable "sg_name" {
  type = string
  description = "Security group name"
}

variable "vnet_name" {
  type = string
  description = "Virtual network name"
}

variable "vnet_tags" {
  type = map(string)
  description = "Virtual network tags"
}

variable "cidr_block" {
  type = string
  description = "CIDR block for address space in virtual network"
}

variable "subnet_1_name" {
  type = string
  description = "Name of the first subnet"
}

variable "subnet_1_cidr" {
  type = string
  description = "CIDR of the first subnet"
}

variable "subnet_2_name" {
  type = string
  description = "Name of the second subnet"
}

variable "subnet_2_cidr" {
  type = string
  description = "CIDR of the second subnet"
}

variable "sa_name" {
  type = string
  description = "Storage account name"
}


resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.azure_location_name
  tags = var.rg_tags
}

resource "azurerm_network_security_group" "sg" {
  name                = var.sg_name
  location            = var.azure_location_name
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_network_security_rule" "AllowSSH" {
  resource_group_name = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.sg.name
  access = "Allow"
  description = "SSH access"
  destination_address_prefix = "*"
  destination_port_range = 22
  direction = "Inbound"
  name = "AllowSSH"
  priority = 100
  protocol = "Tcp"
  source_address_prefix = "*"
  source_port_range = "*"
}

resource "azurerm_network_security_rule" "AllowS3" {
  resource_group_name = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.sg.name
  access = "Allow"
  description = "S3 access"
  destination_address_prefix = "*"
  destination_port_range = 9000
  direction = "Inbound"
  name = "AllowS3"
  priority = 103
  protocol = "Tcp"
  source_address_prefix = "*"
  source_port_range = "*"
}

resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  location            = var.azure_location_name
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = [var.cidr_block]
  tags = var.vnet_tags
}

resource "azurerm_subnet" "subnet_1" {
  name                 = var.subnet_1_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.subnet_1_cidr]
}

resource "azurerm_subnet" "subnet_2" {
  name                 = var.subnet_2_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.subnet_2_cidr]
}

resource "azurerm_subnet_network_security_group_association" "sgtosubnet1" {
  subnet_id                 = azurerm_subnet.subnet_1.id
  network_security_group_id = azurerm_network_security_group.sg.id
}

resource "azurerm_subnet_network_security_group_association" "sgtosubnet2" {
  subnet_id                 = azurerm_subnet.subnet_2.id
  network_security_group_id = azurerm_network_security_group.sg.id
}

resource "azurerm_storage_account" "sa" {
  name                     = var.sa_name
  location                 = var.azure_location_name
  resource_group_name      = azurerm_resource_group.rg.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
