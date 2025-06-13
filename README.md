# IoT Device Status Sensor API

A FastAPI-based backend service for managing and retrieving IoT device status data.  

## Setup Instructions

### Prerequisites

- Python 3.10+
- Docker 
- `pip` for installing dependencies

### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/KOYYADOONDYSAIVYSHNAVI/iot-device-status.git
   cd iot-device-status-sensor
    ```

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application locally:
    ```bash
    uvicorn main:app --reload
    ```

4. Access API docs at `http://localhost:8000/docs`


### Using Docker
1. Build and run with Docker:
    ``` bash
    docker build -t IOT-DEVICE-STATUS .
    docker run -p 8000:8000 IOT-DEVICE-STATUS
    ```
2. Use Docker compose for local development:
    ``` bash
    docker compose up --build
    ```

## Design Decisions:
- FastAPI for high-performance asynchronous API development.

- SQLAlchemy ORM for database interaction, supporting SQLite for development.

- Pydantic models for data validation with custom validators (e.g., timestamps not in future).

- Dockerized environment for consistent deployment and testing.

- Separate test database to isolate test data from production data.

- Pytest for unit and integration tests.

- Modular architecture: routers, models, database sessions organized in separate modules.

## Running Tests
### Locally (without Docker)
1. Run specific tests:
    ``` bash
    pytest tests/test_validators.py
    pytest routers/test_status.py
    ```

### Using Docker
1. Build and run tests inside the Docker container:
    ```bash
    docker build -t IOT-DEVICE-STATUS .
    docker run IOT-DEVICE-STATUS pytest
    ``` 
## CI/CD Integration
### Overview
This project can be integrated into a CI/CD pipeline to automate:

- Code linting and formatting

- Running unit and integration tests

- Deploying to staging/production environments

### Using GitHub Actions
1. We can add a .github/workflows/ci.yml workflow like:
    ``` bash
      name: CI
      on:
        push:
          branches:
            - main
        pull_request:
      jobs:
        build-and-test:
          runs-on: ubuntu-latest

          steps:
            - uses: actions/checkout@v3

            - name: Set up Python
              uses: actions/setup-python@v4
              with:
                python-version: '3.10'

            - name: Install dependencies
              run: pip install -r requirements.txt

            - name: Run tests
              run: pytest unittests/test_validators.py routers/test_status.py
   
            - name: Running the app
              run: uvicorn main:app --host 0.0.0.0 --port 8000

      
    ```
