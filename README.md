# Desarrollado por
## Abdi Daniel Escobar
## Sebastián Gómez
## Andrés Girón

# TaskFlow - Task Management Application

A Flask-based task management system that allows users to create, manage and track their tasks.

## Features
- User authentication (signup/login/logout)
- Create, read, update and delete tasks
- Mark tasks as complete/incomplete
- Task due dates
- Secure password handling
- User-specific task management

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
rye sync
```

3. Configure environment variables:
```bash
export FLASK_APP=src/taskflow/run.py
export DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/taskflow
export SECRET_KEY=your-secret-key
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## Available Routes
- GET / - Home page with task list
- GET/POST /login - User login
- GET/POST /signup - User registration
- GET /logout - User logout
- GET/POST /task/<slug> - View/edit task
- POST /delete_task/<slug> - Delete task
- GET/POST /admin/task - Create new task

## Database Models
- User: Authentication and user management
- Task: Task management with title, description, due date, and completion status

