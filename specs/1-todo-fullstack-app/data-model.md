# Data Model: Phase II – Todo Full-Stack Web Application

**Date**: 2026-01-08
**Feature**: 1-todo-fullstack-app
**Model Version**: 1.0

## Entity-Relationship Overview

The data model consists of two primary entities: User and Task. Each user can own multiple tasks, but each task belongs to exactly one user. This ensures proper data isolation between users.

## Entity Definitions

### User Entity

Represents a registered user with authentication credentials and identity information.

**Attributes:**
- `id`: UUID (Primary Key)
  - Unique identifier for the user
  - Auto-generated on creation
- `email`: String (Unique, Indexed)
  - User's email address for authentication
  - Required field, validated format
- `created_at`: DateTime (Indexed)
  - Timestamp when the user account was created
  - Auto-populated on creation
- `updated_at`: DateTime
  - Timestamp when the user account was last updated
  - Auto-updated on modifications

**Relationships:**
- One-to-Many: User → Tasks (via user_id foreign key)

### Task Entity

Represents a todo task with properties including title, description, completion status, creation date, and user ID reference.

**Attributes:**
- `id`: UUID (Primary Key)
  - Unique identifier for the task
  - Auto-generated on creation
- `title`: String (Not Null)
  - Title/description of the task
  - Required field, minimum length validation
- `description`: Text (Nullable)
  - Optional detailed description of the task
  - Can be null or empty
- `completed`: Boolean (Default: false)
  - Status indicating whether the task is completed
  - Default value is false
- `user_id`: UUID (Foreign Key to users.id, Indexed)
  - Reference to the user who owns this task
  - Required field, enforces data isolation
- `created_at`: DateTime (Indexed)
  - Timestamp when the task was created
  - Auto-populated on creation
- `updated_at`: DateTime
  - Timestamp when the task was last updated
  - Auto-updated on modifications

**Relationships:**
- Many-to-One: Task → User (via user_id foreign key)

## Database Schema (SQLModel)

### User Model
```python
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True, index=True, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("updated_at", DateTime, nullable=False))

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
```

### Task Model
```python
class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(sa_column=Column("title", String, nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column("description", Text))
    completed: bool = Field(default=False, sa_column=Column("completed", Boolean, nullable=False))
    user_id: UUID = Field(foreign_key="user.id", sa_column=Column("user_id", UUID, index=True, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("updated_at", DateTime, nullable=False))

    # Relationship to user
    user: User = Relationship(back_populates="tasks")
```

## Indexes and Constraints

### Indexes
1. `users.email` - Unique index for fast email lookups during authentication
2. `users.created_at` - Index for chronological queries
3. `tasks.user_id` - Index for efficient user-based filtering
4. `tasks.completed` - Index for filtering completed/incomplete tasks
5. `tasks.created_at` - Index for chronological task ordering

### Constraints
1. `users.email` - Unique constraint to prevent duplicate accounts
2. `tasks.user_id` - Foreign key constraint ensuring referential integrity
3. `tasks.title` - Not null constraint to ensure all tasks have a title
4. `tasks.completed` - Boolean constraint with default false value

## Data Access Patterns

### Common Queries
1. **Get user's tasks**: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
2. **Get specific task**: `SELECT * FROM tasks WHERE id = ? AND user_id = ?`
3. **Create task**: `INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)`
4. **Update task**: `UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ? AND user_id = ?`
5. **Delete task**: `DELETE FROM tasks WHERE id = ? AND user_id = ?`

### Security Enforcement
- All queries that access tasks must include the user_id filter to ensure data isolation
- Backend services validate that the authenticated user owns the requested resources
- Database constraints prevent direct manipulation of user_id after creation

## Migration Strategy

### Initial Schema Creation
1. Create users table with basic user information
2. Create tasks table with foreign key reference to users
3. Apply indexes for performance optimization
4. Set up foreign key constraints for data integrity

### Future Considerations
- Add soft delete capability if needed (deleted_at field)
- Add category/tags support if requirements expand
- Add due date field for task scheduling if needed
- Add priority field for task importance ranking