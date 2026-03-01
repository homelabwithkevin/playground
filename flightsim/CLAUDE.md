# Flight Sim Project

## Overview
A FastAPI-based flight simulator calculator application designed to run on AWS Lambda.

## Tech Stack
- **Framework**: FastAPI
- **Language**: Python 3.14+
- **Deployment**: AWS Lambda (SAM)
- **Package Manager**: pip
- **Testing**: pytest

## Project Structure
```
flightsim/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── samconfig.toml          # SAM configuration
├── tests.py                # Test suite
└── README.md               # Project documentation
```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   fastapi dev .\fast.py
   ```

4. Run tests:
   ```bash
   pytest tests.py
   ```

## Code Conventions

- Use type hints for all function parameters and return values
- Keep endpoint handlers focused and thin
- Use Pydantic models for request/response validation
- Organize related endpoints with APIRouter
- Document API endpoints with docstrings and OpenAPI tags
- Use async/await for I/O operations

## AWS Lambda Deployment

- Update `samconfig.toml` with deployment parameters
- Deploy with: `sam deploy`
- The app handler is configured in SAM template
- Lambda function should use the FastAPI app as the handler via Mangum adapter

## Git Workflow

- Work on feature branches (e.g., `feature/flight-sim-lambda`)
- Create pull requests to `main` for review
- Keep commits atomic and descriptive
- Reference issue numbers in commit messages when applicable

## Testing

- Write tests for all API endpoints
- Aim for good coverage of business logic
- Use pytest fixtures for common test setup
- Mock external dependencies (AWS services, databases)

## Dependencies Management

- Keep `requirements.txt` minimal and up-to-date
- Pin major versions for stability
- For Lambda: consider package size for deployment
- Review AWS Lambda layers for heavy dependencies

## Common Tasks

- **Add new endpoint**: Create route in main.py or separate router, add corresponding tests
- **Update dependencies**: Modify requirements.txt and test thoroughly
- **Deploy to Lambda**: Run `sam deploy` after testing locally
