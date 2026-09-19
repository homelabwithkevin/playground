variable "region" {
  type        = string
  description = "Azure region where resources will be deployed"
}

variable "amount" {
  type        = string
  description = "Budget amount threshold"
}

variable "budget" {
  type        = list(string)
  description = "List of budget names or categories to track"
}

variable "start_date" {
  type        = string
  description = "Budget period start date (YYYY-MM-DD format)"
}

variable "contact_emails" {
  type        = list(string)
  description = "Email addresses for budget alert notifications"
}

variable "subscription_id" {
  type        = string
  description = "Azure subscription ID"
}

variable "resource_groups" {
  type        = list(string)
  description = "List of resource group names to apply budget to"
}