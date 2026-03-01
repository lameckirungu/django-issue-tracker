# Issue Tracking System

> A web-based issue tracking system built with Django and Django REST Framework

## About

This is a learning project to build a full-featured ticketing system with:

- User authentication and role-based permissions
- Ticket creation, assignment, and status management
- Both HTML templates and RESTful API endpoints

## Planned Features

- User authentication (registration, login/logout)
- Ticket CRUD operations
- Role-based permission system
- Status tracking (open, in_progress, closed)
- Priority levels (low, medium, high)
- Assignment system
- Dashboard and reporting
- RESTful API with DRF
- API token authentication

## Tech Stack

- **Backend:** Python, Django 4.x
- **API:** Django Rest Framework
- **Database:** PostgreSQL (production), SQLite (development)
- **Frontend:** Django Templates, HTML/CSS

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Redirect to Swagger docs (`/api/docs/`) |
| `GET` | `/api/docs/` | Interactive API docs |
| `GET` | `/api/redoc/` | ReDoc API docs |
| `GET` | `/api/schema/` | OpenAPI schema |
| `GET` | `/api/v1/tickets/` | List all tickets (auth required) |
| `POST` | `/api/v1/tickets/` | Create a new ticket (auth required) |
| `GET` | `/api/v1/tickets/{id}/` | Retrieve a specific ticket (auth required) |
| `PUT`/`PATCH` | `/api/v1/tickets/{id}/` | Update a specific ticket (auth required) |
| `DELETE` | `/api/v1/tickets/{id}/` | Delete a specific ticket (auth required) |
| `POST` | `/api/v1/auth/register/` | User registration |
| `POST` | `/api/v1/auth/login/` | User login (API token) |
| `POST` | `/api/v1/auth/logout/` | User logout (API token) |


## Project Structure

The project is divided into three core Django apps:

* **`accounts/`**: Handles user authentication, models, permissions logic.
* **`tickets`**: Contains the main business domain logic, includding the `Ticket` model, views, and serializers.
* **`Core/`**: For shared utilities

## 📅 5-Week Project Plan Overview

| Week | Focus Area | Key Deliverables |
| :--- | :--- | :--- |
| **Week 1** | Foundation | Project setup, settings, auth configuration, `Ticket` model, migrations. |
| **Week 2** | Core Functionality | Ticket CRUD (HTML views), Basic permissions, Ticket list & detail pages. |
| **Week 3** | DRF Integration | Serializers, Viewsets, API permissions, API testing. |
| **Week 4** | Polishing & Development | Template cleanup, Error handling, Basic tests, Deployment, Write README. |
| **Week 5** | Testing, Review, and Polish | Comprehensive unit and integration testing, bug fixing, final UI/UX polish. |
