resource "azurerm_resource_group" "resource-group" {
  for_each = toset(var.resource_groups)
  name     = each.key
  location = var.region
}

