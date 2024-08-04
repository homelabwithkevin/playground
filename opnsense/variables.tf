variable "api_key" {}
variable "api_secret" {}
variable "haproxy" {}
variable "ovh" {}
variable "ovh_2024" {}
variable "ovh_seedbox" {}

variable "cloud_homelabwithkevin" {
  type    = list(string)
  default = ["coder"]
}

variable "homelabwithkevin" {
  type = list(string)
  default = [
    "seedbox",
    "sonarr",
    "radarr",
    "rutorrent"
  ]
}

variable "haproxy_homelabwithkevin" {
  type = list(string)
  default = [
    "coder",
    "ovh-nextcloud"
  ]
}