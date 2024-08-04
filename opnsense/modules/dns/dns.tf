resource "opnsense_unbound_host_override" "dns" {
  enabled     = true
  description = var.description

  hostname = var.hostname
  domain   = var.domain
  server   = var.server
}

variable "description" {}
variable "hostname" {}
variable "domain" {}
variable "server" {}