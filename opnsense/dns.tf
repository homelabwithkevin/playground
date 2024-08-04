resource "opnsense_unbound_host_override" "coder-hlb" {
  enabled = true
  description = "coder-hlb"

  hostname = "coder"
  domain = "cloud.homelabwithkevin.com"
  server = var.ovh_2024
}