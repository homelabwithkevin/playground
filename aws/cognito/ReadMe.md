# ReadMe

Simple implementation of login/logout with
- Cognito Hosted UI
- htmx
- AWS Lambda
- AWS HTTP API Gateway

# Notes
If you use `AliasAttributes` with both `email` and `preferred_username`, you will need to use the `preferred_username` to login. `email` will not work.

## Deployment
1. sam build; sam deploy
2. Get outputs
3. `sam build`
4. Use `sam deploy --guided` and replace with your own values
5. Delete the `parameter_overrides` in the `samconfig.toml` file

# Authorization Flow
1. `/login`
2. `/callback`
3. `/dashboard`

# Docs
- https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
- https://repost.aws/questions/QU4VpxEkw_Q6yQotN5JhkBEA/lambda-function-url-not-returning-multiple-cookies
- https://stackoverflow.com/questions/46619746/aws-cognito-how-to-create-pool-allowing-sign-up-with-email-address-using-clou
- https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html

## Commands
1. `sam sync --stack-name hlb-cognito-develop`
