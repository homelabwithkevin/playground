module "cloud-homelabwithkevin" {
  for_each    = toset(var.cloud_homelabwithkevin)
  source      = "./modules/dns"
  description = "${each.key}-hlb-tf"
  hostname    = each.key
  domain      = "cloud.homelabwithkevin.com"
  server      = var.ovh_2024
}