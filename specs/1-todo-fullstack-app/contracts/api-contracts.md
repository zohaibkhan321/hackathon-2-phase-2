# API Contracts: Phase II – Todo Full-Stack Web Application

**Date**: 2026-01-08
**Feature**: 1-todo-fullstack-app
**Version**: 1.0

## Overview

This document defines the API contracts for the Phase II Todo Full-Stack Web Application. All endpoints require JWT authentication in the Authorization header, except for authentication endpoints.

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token_here>
```

Unauthenticated requests return `401 Unauthorized`.

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid input",
  "details": "Email format incorrect or password too weak"
}
```

#### POST /api/auth/login
Log in to an existing account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

### Tasks

#### GET /api/tasks
Retrieve all tasks for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token_here>
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Sample task",
      "description": "Optional task description",
      "completed": false,
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-08T10:00:00Z"
    }
  ]
}
```

#### POST /api/tasks
Create a new task for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token_here>
```

**Request:**
```json
{
  "title": "New task",
  "description": "Optional description"
}
```

**Response (201 Created):**
```json
{
  "task": {
    "id": "uuid-string",
    "title": "New task",
    "description": "Optional description",
    "completed": false,
    "user_id": "user-uuid-string",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z"
  }
}
```

#### PUT /api/tasks/{id}
Update an existing task for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token_here>
```

**Request:**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true,
    "user_id": "user-uuid-string",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T11:00:00Z"
  }
}
```

#### DELETE /api/tasks/{id}
Delete a task for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token_here>
```

**Response (204 No Content)**

#### PATCH /api/tasks/{id}/complete
Toggle the completion status of a task.

**Headers:**
```
Authorization: Bearer <jwt_token_here>
```

**Request:**
```json
{
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Sample task",
    "description": "Optional task description",
    "completed": true,
    "user_id": "user-uuid-string",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T11:00:00Z"
  }
}
```

## Error Responses

Standard error response format:

```json
{
  "error": "Error message",
  "status_code": 400,
  "details": "Additional details if applicable"
}
```

## Common Status Codes

- `200 OK`: Successful request with response body
- `201 Created`: Successful creation of a resource
- `204 No Content`: Successful request with no response body
- `400 Bad Request`: Invalid request parameters or body
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Requested resource does not exist
- `500 Internal Server Error`: Unexpected server error