# my-python-app

A FastAPI Python application with comprehensive CI/CD pipeline and Docker support.

## Features

- FastAPI web framework
- Docker containerization with multi-stage builds
- Docker Compose for local development
- Comprehensive CI/CD pipeline with GitHub Actions
- Testing with pytest and coverage reporting
- Code quality checks (black, flake8, mypy)
- Security scanning (bandit, safety)
- Health check endpoints
- Non-root Docker user for security

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (optional)

## Installation

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

### Docker

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Or build and run manually:
```bash
docker build -t my-python-app .
docker run -p 8000:8000 my-python-app
```

## API Endpoints

- `GET /` - Root endpoint that returns a greeting
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=app --cov-report=html
```

## Code Quality

### Formatting
```bash
black app tests
```

### Linting
```bash
flake8 app tests
```

### Type Checking
```bash
mypy app
```

### Security Checks
```bash
bandit -r app
safety check
```

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions CI/CD pipeline that:

- Runs tests on Python 3.10, 3.11, and 3.12
- Performs code quality checks (black, flake8, mypy)
- Runs security scans (bandit, safety)
- Builds and caches Docker images
- Pushes Docker images to GitHub Container Registry (on main branch)

### Workflow Triggers

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

## Project Structure

```
.
├── app/                    # Application code
│   └── main.py            # FastAPI application entry point
├── tests/                 # Test files
│   └── test_main.py       # Tests for main application
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── pytest.ini             # Pytest configuration
├── .flake8                # Flake8 configuration
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## Environment Variables

- `PYTHONUNBUFFERED=1` - Ensures unbuffered output from Python

## Security Notes

- Docker images run with a non-root user (`appuser` with UID 1000)
- Health checks are configured for container orchestration
- All dependencies are pinned to specific versions
- Multi-stage builds reduce final image size and attack surface

## Development Workflow

1. Create a feature branch from `develop`
2. Make changes and commit
3. Push to your branch
4. Create a pull request to `develop`
5. Wait for CI/CD checks to pass
6. After review and approval, merge to `develop`
7. Periodically create release pull requests from `develop` to `main`

## License

MIT

## Support

For issues or questions, please create an issue in the repository.
