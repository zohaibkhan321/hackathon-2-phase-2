# Quickstart Guide: Phase II – Todo Full-Stack Web Application

**Date**: 2026-01-08
**Feature**: 1-todo-fullstack-app
**Version**: 1.0

## Prerequisites

Before getting started with the Phase II Todo Full-Stack Web Application, ensure you have the following installed:

### System Requirements
- Node.js v18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Git for version control
- Package managers: npm/yarn/pnpm for frontend, pip/poetry for backend

### Environment Setup
- Database URL (DATABASE_URL) pointing to Neon Serverless PostgreSQL
- Better Auth secret (BETTER_AUTH_SECRET) for JWT signing
- Environment variables configured for development

## Repository Structure

The application follows a monorepo structure with clear separation between frontend and backend:

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
        └── ...
```

## Development Setup

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Initialize the project based on the spec-driven approach
# The structure is already prepared according to the specification
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend/

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your actual values:
# DATABASE_URL=your_neon_postgres_url
# BETTER_AUTH_SECRET=your_jwt_secret

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend/

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local file with your actual values:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api
# NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/auth

# Start the frontend development server
npm run dev
```

## Running the Application

### Development Mode
1. Start the backend server (port 8000 by default)
2. Start the frontend server (port 3000 by default)
3. Access the application at http://localhost:3000

### Production Build
```bash
# Build the frontend
cd frontend/
npm run build

# The backend can be deployed as a uvicorn application
# Follow your hosting provider's instructions for FastAPI deployment
```

## Key Features Implementation

### Authentication Flow
1. User registers/login through Better Auth
2. JWT token is issued and stored securely
3. All API requests include the Authorization header with Bearer token
4. Backend validates JWT and extracts user identity

### Task Management
1. Users can create, read, update, and delete their own tasks
2. Data isolation ensures users can only access their own tasks
3. Tasks are persisted in Neon PostgreSQL database
4. Responsive UI works on mobile and desktop devices

### API Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PATCH /api/tasks/:id/complete` - Toggle task completion

## Testing

### Backend Tests
```bash
# Run backend tests
cd backend/
python -m pytest tests/
```

### Frontend Tests
```bash
# Run frontend tests
cd frontend/
npm run test
```

## Configuration

### Environment Variables

#### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT signing
- `ENVIRONMENT`: Development/production flag

#### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth base URL

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify DATABASE_URL is correctly set
   - Check that your Neon PostgreSQL instance is accessible
   - Ensure firewall rules allow connections

2. **Authentication Issues**
   - Confirm BETTER_AUTH_SECRET matches between frontend and backend
   - Verify JWT token is properly included in requests
   - Check that Better Auth is properly configured

3. **Cross-Origin Issues**
   - Ensure CORS is properly configured in the backend
   - Verify frontend and backend URLs are correctly set

### Development Tips

1. Use the spec-driven approach: Refer to `specs/1-todo-fullstack-app/spec.md` for requirements
2. Follow the plan: Consult `specs/1-todo-fullstack-app/plan.md` for architecture decisions
3. Check data model: Reference `specs/1-todo-fullstack-app/data-model.md` for database structure
4. Validate against success criteria: Ensure implementation meets all measurable outcomes from the spec

## Next Steps

1. Review the complete feature specification
2. Examine the implementation plan for architectural decisions
3. Understand the data model for database operations
4. Follow the contracts documentation for API specifications
5. Begin with the tasks defined in `specs/1-todo-fullstack-app/tasks.md` (to be generated)