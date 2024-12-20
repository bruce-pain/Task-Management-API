# Task Management API

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Environment Variables](#environment-variables)
    - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
    - [Authentication](#authentication)
    - [Task Endpoints](#task-endpoints)
    - [Additional Features](#additional-features)
- [Error Handling and Validation](#error-handling-and-validation)
- [Scalability and Optimization](#scalability-and-optimization)
<!-- - [Testing](#testing) -->

---

## Project Overview

This is a RESTful API built for a task management system that allows users to manage tasks, assign deadlines, and mark tasks as completed. It is built with Python and FastAPI, featuring robust error handling, authentication, and scalable design.

## Features

- User Authentication with JWT
- CRUD operations for task management
- Task assignment, tagging, and prioritization
- Pagination and filtering options for large task lists
- Secure handling of user data with comprehensive error management

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Database**: PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone https://github.com/bruce-pain/Task-Management-API
cd Task-Management-API
```
2. Set up a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Database
Create a PostgreSQL database locally or use a live database (like Supabase)

### Environment Variables

Create a `.env` file with the configuration defined in `.env.sample`

### Migrations
Before running the application, you should make a migration

```bash
alembic revision --autogenerate -m 'initial migration'
alembic upgrade head
```

### Running the Application

To start the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Full API Documentation (local): [https://localhost:8000/docs](https://localhost:8000/docs)

### Authentication

- **POST /users/register** - Register a new user
- **POST /users/login** - Authenticate a user and receive a JWT token

### Task Endpoints

- **POST /tasks** - Create a new task
- **GET /tasks** - Retrieve all tasks with pagination (e.g., `/tasks?page=1&limit=20`)
- **GET /tasks/{id}** - Retrieve a task by its ID
- **PUT /tasks/{id}** - Update a task by ID
- **DELETE /tasks/{id}** - Delete a task by ID

### Additional Features

- [ ] **Task Filtering** - Filter tasks by status, priority, or tags (e.g., `/tasks?status=pending&priority=high`)
- [ ] **Task Sharing** - Share tasks with others using their email addresses

## Error Handling and Validation

This API includes robust error handling with detailed feedback for:

- Invalid data inputs
- Missing resources (e.g., task not found)
- Unexpected server errors

## Scalability and Optimization

- [x] **Pagination** on task listing endpoints for handling large numbers of tasks
- [x] **Database indexing** to improve performance on frequent queries (e.g., status or due date indexing)
- [ ] **Optional Caching** using Redis for high-traffic data

<!-- ## Testing -->
<!---->
<!-- Unit tests are available for all endpoints. To run the tests: -->
<!-- ```bash -->
<!-- pytest -->
<!-- ``` -->

