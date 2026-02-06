<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → Spec-driven development as the single source of truth
                    [PRINCIPLE_2_NAME] → Zero manual coding by the user
                    [PRINCIPLE_3_NAME] → Deterministic, reviewable agentic workflow
                    [PRINCIPLE_4_NAME] → Secure-by-default full-stack architecture
                    [PRINCIPLE_5_NAME] → Clear separation of concerns
                    [PRINCIPLE_6_NAME] → Human-in-the-loop validation
Added sections: Development Discipline, Scope Enforcement, Architecture Standards, Authentication & Security Standards, API Standards, Frontend Standards, Backend Standards, Database Standards, Workflow Enforcement, Disallowed Actions, Success Criteria
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ updated
Follow-up TODOs: None
-->
# Hackathon 2 – Phase II Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-driven development as the single source of truth
All development must follow specifications as the authoritative source. Code implementations must strictly adhere to written specs, with any deviations requiring spec updates first. This ensures deterministic, reviewable development that aligns with intended functionality.

### Zero manual coding by the user
The development process must be fully automated through Claude Code agents. Users should not write code directly but instead provide requirements and specifications that agents will implement. This ensures consistent, reproducible, and reviewable development practices.

### Deterministic, reviewable agentic workflow
All development workflows must be predictable, auditable, and reproducible. Every change must follow a clear, traceable path from specification to implementation with proper documentation and version control. This enables effective review and validation of all changes.

### Secure-by-default full-stack architecture
Security must be built into the architecture from the ground up. All components must follow security best practices by default, including authentication, authorization, data validation, and secure communication patterns. Security cannot be an afterthought but must be foundational.

### Clear separation of concerns
Frontend, backend, database, and authentication layers must have well-defined boundaries and responsibilities. Each component must have a single, clear purpose with minimal coupling between layers. This ensures maintainability, testability, and scalability.

### Human-in-the-loop validation
Critical decisions and complex implementations must involve human oversight and validation. The agentic workflow must include checkpoints for human review and approval of architectural decisions, security implementations, and complex business logic.

## Development Discipline

- Specs must be written or updated before implementation
- Claude Code must always reference specs using @specs/... paths
- If a requirement is unclear or missing, update or create a spec before coding
- Implementation must strictly follow Spec-Kit Plus conventions
- CLAUDE.md files override default assumptions at all levels

## Scope Enforcement

- Only Phase II features may be implemented
- No Phase III (AI chatbot), Phase IV (Kubernetes), or Phase V (Cloud/Kafka) work
- No mobile apps, realtime sync, payments, or RBAC
- REST API endpoints must remain exactly as specified

## Architecture Standards

- Monorepo structure is mandatory
- Frontend: Next.js 16+ App Router
- Backend: Python FastAPI
- ORM: SQLModel only
- Database: Neon Serverless PostgreSQL only
- Frontend must never access the database directly
- Backend must never trust client-provided identity data

## Authentication & Security Standards

- Authentication handled via Better Auth on frontend
- JWT tokens are the only authentication mechanism
- JWT must be sent via Authorization: Bearer <token> header
- FastAPI must verify JWT using shared secret
- Shared secret must come from BETTER_AUTH_SECRET environment variable
- User identity must be extracted from JWT, never trusted from request body or URL
- All API endpoints require valid JWT authentication
- Requests without valid JWT must return 401 Unauthorized
- Task ownership must be enforced on every CRUD operation

## API Standards

- All routes must be under /api/
- Endpoints must match the provided REST specification exactly
- Responses must be JSON
- Use Pydantic models for request and response schemas
- Proper HTTP status codes must be returned (200, 201, 400, 401, 403, 404)
- API behavior must filter all data by authenticated user only

## Frontend Standards

- Server components by default
- Client components only when required for interactivity
- All API calls must go through a centralized API client
- JWT must be attached automatically to every request
- Tailwind CSS only (no inline styles)
- UI must be responsive and usable on mobile and desktop
- Authentication state managed via Better Auth session

## Backend Standards

- FastAPI application entry via main.py
- SQLModel used for all database interactions
- No raw SQL unless explicitly specified in specs
- Database connection via DATABASE_URL environment variable
- Auth verification implemented via middleware or dependencies
- Errors handled with HTTPException, no stack traces exposed

## Database Standards

- Schema must match @specs/database/schema.md
- tasks table must reference user_id
- Foreign key constraints must be enforced
- Indexes must exist for user_id and completed status
- No in-memory or SQLite database usage

## Workflow Enforcement

1. Read relevant spec(s)
2. Generate an implementation plan
3. Break plan into small, verifiable tasks
4. Implement tasks incrementally via Claude Code
5. Validate behavior against acceptance criteria
6. Update specs if behavior changes

## Disallowed Actions

- Writing code without referencing specs
- Skipping authentication or authorization checks
- Hardcoding secrets or credentials
- Mixing frontend and backend responsibilities
- Implementing undocumented behavior
- Bypassing Spec-Kit Plus structure

## Success Criteria

- Full-stack application runs locally
- Multi-user authentication works correctly
- Users can only access their own tasks
- REST API is fully secured with JWT
- Neon PostgreSQL stores data persistently
- Codebase follows Spec-Kit and CLAUDE.md rules
- Project is reviewable, reproducible, and hackathon-ready

## Governance

The constitution serves as the authoritative guide for all development practices. All team members must adhere to these principles, and any deviations require formal amendment to the constitution. Changes to core principles require explicit approval and proper documentation of rationale and impact.

**Version**: 1.1.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08