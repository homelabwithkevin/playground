module "budgets" {
  source          = "./modules/budget"
  amount          = var.amount
  budget          = var.budget
  start_date      = var.start_date
  contact_emails  = var.contact_emails
  subscription_id = var.subscription_id
}
