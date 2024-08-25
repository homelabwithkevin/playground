variable "rgs" {
  default = [
    "example",
    "example1",
    "example2",
    "example3",
  ]
}

resource "azurerm_resource_group" "resource-group" {
  for_each = toset(var.rgs)
  name     = each.key
  location = var.region
}

