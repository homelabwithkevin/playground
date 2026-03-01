# Read Me
Messing around with FastAPI. Huge kudos to Geri at [Next Sim Flight](https://www.nextsimflight.com/)

# AI Usage
- Used a little bit of Claude Code to get me started. As well as gemma3 in OpenWebUI.
- Used to create doc strings
- Used to review code.

# Commands

## Development
- `fastapi dev ./code/fast.py` - Start FastAPI dev server

## AWS SAM
- `sam build` - Build the application
- `sam validate` - Validate the SAM template
- `sam local start-api` - Start API locally on http://localhost:3000, requires Docker
- `sam local start-lambda` - Start Lambda runtime locally, requires Docker
- `sam sync --watch --stack-name flightsim-hlb` - Sync local changes to AWS during development
- `sam deploy` - Deploy to AWS
- `sam deploy --guided` - Deploy to AWS via Guided
- `sam delete` - Delete the CloudFormation stack

# Sources

- https://www.nextsimflight.com/
- https://ourairports.com/airports.html
- https://en.wikipedia.org/wiki/Haversine\_formula
- https://www.geeksforgeeks.org/python/apply-a-function-to-each-row-or-column-in-dataframe-using-pandas-apply/
- https://www.geeksforgeeks.org/pandas/drop-rows-from-the-dataframe-based-on-certain-condition-applied-on-a-column/
