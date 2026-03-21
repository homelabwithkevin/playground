# ReadMe
Hosts prod and non-prod stacks for the cat newsletter.

They share database; develop has read-only access.

| File | Description |
| ---- | ----------- |
| template.yaml | Unified template for both prod and develop environments (parametrized by `Environment` variable) |
| samconfig.yaml | SAM configuration with environment-specific stacks |

# Development & Deployment
I use the prod account for both environment. Develop has `Read Only` to the production DynamoDB Tables.

## Prod
```bash
sam sync --stack-name hlb-mailtrap-s3-prod --watch
sam build -t template.yaml
sam deploy --config-env prod
```

## Develop
```bash
sam sync --stack-name hlb-mailtrap-s3-develop --watch
sam build -t template.yaml
sam deploy --config-env develop
```