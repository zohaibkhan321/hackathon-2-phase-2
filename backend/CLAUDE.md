# Backend CLAUDE.md

This is the Claude Code rules file for the backend component of the Todo Full-Stack Web Application.

## Backend Specific Rules

- All API endpoints must validate JWT tokens before processing requests
- Database operations must use SQLModel for type safety
- All user data must be filtered by authenticated user ID
- Error responses must follow the standardized format
- Authentication logic must use the shared BETTER_AUTH_SECRET