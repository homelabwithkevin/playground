terraform {
  required_providers {
    opnsense = {
      source  = "browningluke/opnsense"
    }
  }
}

provider "opnsense" {
  uri = "https://192.168.2.1:81"
  api_key = var.api_key
  api_secret = var.api_secret
  allow_insecure = true
}