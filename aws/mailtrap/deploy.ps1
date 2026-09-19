# Prod
## Build
sam build -t .\template.yaml
sam deploy --config-env prod --config-file .\samconfig.yaml --template .\template.yaml

## Sync / Live Edit
sam sync -t .\template.yaml --watch --code --stack-name hlb-mailtrap-s3-prod

# Develop
## Build
sam build -t .\template-develop.yaml
sam deploy --config-env develop --config-file .\samconfig.yaml --template .\template-develop.yaml

## Sync / Live Edit
sam sync -t .\template-develop.yaml --watch --code --stack-name hlb-mailtrap-s3-develop