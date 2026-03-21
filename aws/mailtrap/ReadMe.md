# ReadMe
Hosts prod and non-prod stacks for the cat newsletter.

They share database; develop has read-only access.

| File | Description |
| ---- | ----------- |
| template.yaml | Unified template for both prod and develop environments (parametrized by `Environment` variable) |
| samconfig.yaml | SAM configuration with environment-specific stacks |

# Development
## Prod
```bash
sam sync --stack-name hlb-mailtrap-s3-prod --watch
```

## Develop
```bash
sam sync --stack-name hlb-mailtrap-s3-develop --watch
```

# Deployment
## Prod
```bash
sam build -t template.yaml
sam deploy --config-env prod
```

## Develop
```bash
sam build -t template.yaml
sam deploy --config-env develop
```