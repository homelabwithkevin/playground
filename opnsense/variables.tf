variable "api_key" {}
variable "api_secret" {}
variable "ovh_2024" {}

variable "homelabwithkevin" {
  type        = list(string)
  description = "list of names"
  default     = ["coder"]
}