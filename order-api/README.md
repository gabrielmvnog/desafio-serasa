# Order API

- [Order API](#order-api)
  - [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Tests and Linting](#tests-and-linting)
    - [Unit Tests](#unit-tests)
    - [Integration Tests](#integration-tests)
    - [Linting](#linting)

## Getting Started

The User API is a microservice-based architecture that enables the management of orders.

## Installation

To install the User API, follow the steps below:

1. Set up the Python environment:

```shell
pyenv shell 3.11
poetry env use 3.11
```

1. Install the project dependencies:

```shell
    poetry install
```

## Tests and Linting

This project includes two types of tests: unit tests and integration tests. Additionally, it provides linting capabilities for code quality checks.

### Unit Tests

To run the unit tests, execute the following command:

```shell
make test
```

### Integration Tests

The integration tests require some additional setup steps before running. Follow the instructions below:

1. Ensure that Docker Compose is up and running:

```shell
docker compose up -d
```

2. Run the database migrations:

```shell
make run-migrations
```

3. Execute the integration tests:

```shell
    make test-integration
```

### Linting

Linting helps maintain code quality and consistency. There are two linting commands available in this project:

- To automatically fix linting issues, use the following command:

```shell
make lint
```

- To check for linting issues without making any changes, typically used in the pipeline, run the command:

```shell
make lint-check
```
