variable "amount" {
  default = "10"
}

variable "budget" {
  default = [
    "90",
    "99",
    "120",
    "150"
  ]
}

variable "start_date" {
  default = "2024-08-01T00:00:00Z"
}

variable "contact_emails" {}

variable "subscription_id" {
  default = "/subscriptions/9b279753-fd83-47fb-9adb-9046023c99e6"
}

module "budgets" {
  source          = "./modules/budget"
  amount          = var.amount
  budget          = var.budget
  start_date      = var.start_date
  contact_emails  = var.contact_emails
  subscription_id = var.subscription_id
}
