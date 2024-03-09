variable "region" {
  default = "us-east-2"
}

variable "repo" {
  default = "repo:homelabwithkevin/playground:*"
}

variable "oidc" {
  default = "arn:aws:iam::195663387853:oidc-provider/token.actions.githubusercontent.com"
}

variable "role_name" {

  default = "playground-sam-gh"
}

variable "api" {
  default = "2hjs3f14o7"
}

variable "stack_name" {

  default = "playground-sam-role"
}

variable "account_number" {
  default = "195663387853"
}

variable "sam_bucket" {
  default = "arn:aws:s3:::aws-sam-cli-managed-default-samclisourcebucket-yqprrstwfbw5"
}