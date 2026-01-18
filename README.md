# Django Task Manager API

Backend API for project-based task management with role-based access control.

The system allows users to create projects, manage project members with roles,
and work with tasks under strict permission rules.

## Key Features

- Project-based task management
- Role-based access control (Owner / Manager / Member)
- JWT authentication
- REST API built with Django REST Framework
- Full test coverage for permissions and business rules

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- Pytest / Django TestCase

## Domain Model

- **Project**
  - Has an owner
  - Contains members and tasks

- **ProjectMember**
  - Connects users to projects
  - Defines role: Owner, Manager, Member

- **Task**
  - Belongs to a project
  - Can be assigned to a project member
  - Has status lifecycle


## Roles

- **Owner**
  - Full access to project, members, and tasks

- **Manager**
  - Can manage project members (except owners)
  - Can fully manage tasks

- **Member**
  - Read-only access to project
  - Can update status of assigned tasks only

## Project Permissions

- Only authenticated users can access projects
- Users see only projects they are members of
- Only project owner can update project data

## Project Member Permissions

- Owner can add/remove managers and members
- Manager can add/remove members only
- Members have read-only access
- Project owner cannot be removed

## Task Permissions

- Tasks are accessible only within their project
- Owner and Manager can:
  - create
  - update
  - delete tasks
- Member can:
  - view tasks
  - update status of assigned tasks only

## Authentication

The API uses JWT authentication.

- Access token
- Refresh token

Authentication is required for all protected endpoints.

## Testing

The project includes full test coverage for:

- Authentication
- Project permissions
- Project member role management
- Task visibility and access rules
- Task creation, update, and status changes

Tests are organized by domain and responsibility.

## How to Run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

```python manage.py test```