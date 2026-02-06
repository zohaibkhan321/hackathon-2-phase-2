# Todo Full-Stack Web Application

A secure, multi-user todo application with Next.js frontend, FastAPI backend, and Neon PostgreSQL database. The application uses Better Auth with JWT tokens for authentication, ensuring each user can only access their own tasks.

## Features

- User registration and authentication with JWT tokens
- Secure task management (create, read, update, delete)
- User isolation - each user can only access their own tasks
- Responsive UI that works on mobile and desktop
- Clean separation of frontend and backend concerns

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT
- **Styling**: Tailwind CSS

## Setup

### Prerequisites

- Node.js v18+
- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend/
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your actual values
```

5. Run the application:
```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend/
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local file with your actual values
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Log in an existing user

### Tasks

- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task for the authenticated user
- `PUT /api/tasks/{id}` - Update an existing task for the authenticated user
- `DELETE /api/tasks/{id}` - Delete a task for the authenticated user
- `PATCH /api/tasks/{id}/complete` - Toggle the completion status of a task

All endpoints except authentication require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token_here>
```

## Environment Variables

### Backend (.env)

- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing
- `ENVIRONMENT` - Development/production flag

### Frontend (.env.local)

- `NEXT_PUBLIC_API_URL` - Backend API base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Better Auth base URL

## Project Structure

```
project-root/
├── backend/                 # FastAPI backend application
│   ├── main.py             # Application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── src/               # Source code
│   │   ├── models/        # SQLModel database models
│   │   ├── services/      # Business logic
│   │   ├── api/           # API route definitions
│   │   └── config/        # Configuration files
│   └── tests/             # Backend tests
├── frontend/              # Next.js frontend application
│   ├── package.json       # Node.js dependencies
│   ├── next.config.js     # Next.js configuration
│   ├── src/              # Source code
│   │   ├── app/          # App Router pages
│   │   ├── components/   # Reusable UI components
│   │   ├── lib/          # Utilities and API clients
│   │   └── styles/       # Global styles
│   └── tests/            # Frontend tests
└── specs/                # Specification files
    └── 1-todo-fullstack-app/
        ├── spec.md        # Feature specification
        ├── plan.md        # Implementation plan
        └── tasks.md       # Implementation tasks
```

## Security Features

- JWT-based authentication with expiration
- User isolation at the service and database level
- Input validation and sanitization
- Secure password hashing
- CORS configured for safe cross-origin requests

## Development

This project follows a spec-driven development approach with the following phases:
1. Specification (spec.md) - Requirements and user stories
2. Planning (plan.md) - Technical architecture and design
3. Tasks (tasks.md) - Implementation breakdown
4. Implementation - Code development

## Contributing

1. Follow the spec-driven development workflow
2. Write tests for new functionality
3. Maintain security best practices
4. Ensure responsive design across devices