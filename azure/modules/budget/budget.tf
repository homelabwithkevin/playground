resource "azurerm_consumption_budget_subscription" "budget-actual" {
  name            = "budget-actual"
  subscription_id = var.subscription_id

  amount     = var.amount
  time_grain = "Monthly"

  time_period {
    start_date = var.start_date
  }

  dynamic "notification" {
    for_each = var.budget
    content {
      enabled        = true
      threshold      = notification.value
      threshold_type = "Actual"
      operator       = "GreaterThan"

      contact_emails = var.contact_emails
    }
  }
}

resource "azurerm_consumption_budget_subscription" "budget-forcast" {
  name            = "budget-forecast"
  subscription_id = var.subscription_id

  amount     = var.amount
  time_grain = "Monthly"

  time_period {
    start_date = var.start_date
  }

  dynamic "notification" {
    for_each = var.budget
    content {
      enabled        = true
      threshold      = notification.value
      threshold_type = "Forecasted"
      operator       = "GreaterThan"

      contact_emails = var.contact_emails
    }
  }
}
