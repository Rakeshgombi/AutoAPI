# AutoAPI

## Overview

The **AutoAPI** is a **Dynamic File-Based API** that is a FastAPI-based project that dynamically generates RESTful APIs based on the directory and file structure of a specified root directory. It allows users to manage resources (directories) and records (JSON files) through a set of predefined and dynamically created endpoints.

This project is designed to be flexible and extensible, making it easy to create, read, update, and delete resources and records without manually defining routes for each resource.

---

## Features

- **Dynamic Route Generation**: Automatically creates API routes based on the directory structure in the root directory.
- **Resource Management**:
  - Create directories for resources.
  - List all available resources.
  - Delete resources.
- **Record Management**:
  - Create, read, update, and delete JSON-based records within resource directories.
  - Pagination support for listing records.
- **Logging**: Centralized logging for better debugging and monitoring.
- **Environment Configuration**: Easily configurable root directory using environment variables.

---

## Installation

### Prerequisites

- Python 3.12 or higher
- `pip` (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AutoAPI
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment:
   - Create a `.env` file in the root directory (if not already present).
   - Define the root directory for resources:
     ```
     ROOT_DIR=./data
     ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

6. Access the API documentation:
   - Open your browser and navigate to `http://127.0.0.1:8000/docs` for the Swagger UI.

---

## Running with Docker

### Prerequisites

- [Docker](https://www.docker.com/) installed on your system.

### Steps

1. Build the Docker image:
   ```bash
   docker build -t autoapi .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 autoapi
   ```

   - The `-p 8000:8000` flag maps port 8000 on your machine to port 8000 in the container.

3. Access the API:
   - Open your browser and navigate to `http://127.0.0.1:8000/docs` for the Swagger UI.

---

## Usage

### Directory Structure

The API dynamically generates routes based on the directory structure under the `ROOT_DIR`. For example:

```
ROOT_DIR/
├── users/
│   ├── 1.json
│   ├── 2.json
├── posts/
│   ├── 1.json
```

- Each directory (e.g., `users`, `posts`) represents a resource.
- Each JSON file within a directory represents a record.

### API Endpoints

#### 1. **Resource Management**

- **Create a Directory**:
  - **Endpoint**: `GET /create-directory/{name}`
  - **Description**: Creates a new directory for the specified resource.
  - **Example**:
    ```bash
    curl -X GET http://127.0.0.1:8000/create-directory/users
    ```

- **List All Resources**:
  - **Endpoint**: `GET /list-resources`
  - **Description**: Lists all available resources (directories) under the root directory.
  - **Example**:
    ```bash
    curl -X GET http://127.0.0.1:8000/list-resources
    ```

- **Delete a Resource**:
  - **Endpoint**: `DELETE /delete-resource/{name}`
  - **Description**: Deletes the specified resource directory.
  - **Example**:
    ```bash
    curl -X DELETE http://127.0.0.1:8000/delete-resource/users
    ```

#### 2. **Dynamic Routes for Records**

For each resource (e.g., `users`), the following routes are dynamically created:

- **List Records**:
  - **Endpoint**: `GET /{resource}`
  - **Query Parameters**:
    - `offset` (optional): Starting index for pagination.
    - `limit` (optional): Number of records to return.
  - **Example**:
    ```bash
    curl -X GET http://127.0.0.1:8000/users?offset=0&limit=10
    ```

- **Get a Record**:
  - **Endpoint**: `GET /{resource}/{entry_id}`
  - **Description**: Retrieves a specific record by its ID.
  - **Example**:
    ```bash
    curl -X GET http://127.0.0.1:8000/users/1
    ```

- **Create a Record**:
  - **Endpoint**: `POST /{resource}`
  - **Description**: Creates a new record in the specified resource.
  - **Example**:
    ```bash
    curl -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d '{"name": "John Doe"}'
    ```

- **Update a Record**:
  - **Endpoint**: `PUT /{resource}/{entry_id}`
  - **Description**: Updates an existing record by its ID.
  - **Example**:
    ```bash
    curl -X PUT http://127.0.0.1:8000/users/1 -H "Content-Type: application/json" -d '{"name": "Jane Doe"}'
    ```

- **Delete a Record**:
  - **Endpoint**: `DELETE /{resource}/{entry_id}`
  - **Description**: Deletes a specific record by its ID.
  - **Example**:
    ```bash
    curl -X DELETE http://127.0.0.1:8000/users/1
    ```

---

## Project Structure

```
AutoAPI/
├── data/                        # Root directory for resources
│   ├── users/                   # Example resource directory
│       ├── 1.json               # Example JSON record
├── routes/
│   ├── apis.py                  # Main API router
│   ├── endpoints/
│   │   ├── __init__.py          # Package initialization
│   │   ├── dynamic_router.py    # Dynamic route generation
│   │   ├── resource_router.py   # Resource management endpoints
│   ├── services/
│   │   ├── __init__.py          # Package initialization
│   │   ├── resource_service.py  # Logic for resource management
│   │   ├── records_service.py   # Logic for record management
├── utils/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration utilities
│   ├── logger.py                # Logging setup
├── main.py                      # Application entry point
├── Dockerfile                   # Docker configuration
├── .dockerignore                # Docker ignore file
├── .gitignore                   # Git ignore file
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata and dependencies
├── README.md                    # Project documentation
├── LICENSE                      # License file
```

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation.
- [Uvicorn](https://www.uvicorn.org/) for the ASGI server.
