module "homelabwithkevin" {
  for_each    = toset(var.homelabwithkevin)
  source      = "./modules/dns"
  description = "${each.key}-hlb"
  hostname    = each.key
  domain      = "cloud.homelabwithkevin.com"
  server      = var.ovh_2024
}