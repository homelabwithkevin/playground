module "haproxy" {
  for_each    = toset(var.haproxy_homelabwithkevin)
  source      = "./modules/dns"
  description = "${each.key}-haproxy-tf"
  hostname    = each.key
  domain      = "homelabwithkevin.com"
  server      = var.haproxy
}