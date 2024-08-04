module "seedbox" {
  for_each    = toset(var.homelabwithkevin)
  source      = "./modules/dns"
  description = "${each.key}-hlb"
  hostname    = each.key
  domain      = "homelabwithkevin.com"
  server      = var.ovh_seedbox
}