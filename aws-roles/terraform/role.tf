resource "aws_iam_role" "role" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRoleWithWebIdentity"
          Condition = {
            StringLike = {
              "token.actions.githubusercontent.com:sub" = var.repo
            }
          }
          Effect = "Allow"
          Principal = {
            Federated = var.oidc
          }
        },
      ]
      Version = "2008-10-17"
    }
  )
  managed_policy_arns  = []
  max_session_duration = 3600
  name                 = var.role_name
  path                 = "/"

  inline_policy {
    name = "apigateway"
    policy = jsonencode(
      {
        Statement = [
          {
            Action = [
              "apigateway:DELETE",
              "apigateway:PUT",
              "apigateway:PATCH",
              "apigateway:POST",
              "apigateway:GET",
            ]
            Effect = "Allow"
            Resource = [
              "arn:aws:apigateway:${var.region}::/apis/${var.api}"
            ]
          },
        ]
        Version = "2012-10-17"
      }
    )
  }
  inline_policy {
    name = "cloudformation"
    policy = jsonencode(
      {
        Statement = [
          {
            Action = [
              "cloudformation:CreateChangeSet",
              "cloudformation:CreateStack",
              "cloudformation:DeleteStack",
              "cloudformation:DescribeChangeSet",
              "cloudformation:DescribeStackEvents",
              "cloudformation:DescribeStacks",
              "cloudformation:ExecuteChangeSet",
              "cloudformation:GetTemplateSummary",
              "cloudformation:ListStackResources",
              "cloudformation:UpdateStack"
            ]
            Effect = "Allow"
            Resource = [
              "arn:aws:cloudformation:${var.region}:${var.account_number}:stack/${var.stack_name}/*",
              "arn:aws:cloudformation:${var.region}:${var.account_number}:stack/aws-sam-cli-managed-default/*"
            ]
          },
          {
            Action = "cloudformation:CreateChangeSet"
            Effect = "Allow"
            Resource = [
              "arn:aws:cloudformation:*:aws:transform/Serverless-2016-10-31"
            ]
          },
        ]
        Version = "2012-10-17"
      }
    )
  }
  inline_policy {
    name = "iam"
    policy = jsonencode(
      {
        Statement = [
          {
            Action = [
              "iam:GetRole",
              "iam:UpdateAssumeRolePolicy",
              "iam:DetachRolePolicy",
              "iam:UntagRole",
              "iam:DeleteRolePolicy",
              "iam:TagRole",
              "iam:CreateRole",
              "iam:DeleteRole",
              "iam:AttachRolePolicy",
              "iam:UpdateRole",
              "iam:PutRolePolicy",
              "iam:GetRolePolicy"
            ]
            Effect   = "Allow"
            Resource = "arn:aws:iam::${var.account_number}:role/${var.stack_name}*"
          },
        ]
        Version = "2012-10-17"
      }
    )
  }
  inline_policy {
    name = "lambda"
    policy = jsonencode(
      {
        Statement = [
          {
            Action = [
              "lambda:AddPermission",
              "lambda:CreateFunction",
              "lambda:DeleteFunction",
              "lambda:GetFunction",
              "lambda:GetFunctionConfiguration",
              "lambda:ListTags",
              "lambda:RemovePermission",
              "lambda:TagResource",
              "lambda:UntagResource",
              "lambda:UpdateFunctionCode",
              "lambda:UpdateFunctionConfiguration"
            ]
            Effect   = "Allow"
            Resource = "arn:aws:lambda:${var.region}:${var.account_number}:function:${var.stack_name}*"
          },
        ]
        Version = "2012-10-17"
      }
    )
  }
  inline_policy {
    name = "s3"
    policy = jsonencode(
      {
        Statement = [
          {
            Action = [
              "s3:DeleteObject",
              "s3:GetObject*",
              "s3:PutObject*",
              "s3:GetBucket*",
              "s3:List*"
            ]
            Effect = "Allow"
            Resource = [
              var.sam_bucket,
              "${var.sam_bucket}/*"
            ]
          },
        ]
        Version = "2012-10-17"
      }
    )
  }
}
