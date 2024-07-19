# Read Me

[![yt-dlp - Deploy to AWS via AWS SAM](https://github.com/homelabwithkevin/playground/actions/workflows/yt-dlp-sam.yaml/badge.svg)](https://github.com/homelabwithkevin/playground/actions/workflows/yt-dlp-sam.yaml)

# Flow

```mermaid
sequenceDiagram
EventBridge->>FuncQuery: Trigger function every X minutes
FuncQuery->>DynamoDB: Query Table
DynamoDB--)FuncQuery: Videos Returned
FuncQuery->>SQS: Add to Queue
SQS->>FuncVideo: Lambda downloads video and its information
FuncVideo->>S3: Save to S3
```