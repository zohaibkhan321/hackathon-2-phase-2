---
id: 1
title: constitution-update-hackathon-project
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: zohaib
command: /sp.constitution
labels: [constitution, hackathon, full-stack, web-application]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
Project: Hackathon 2 – Phase II Todo Full-Stack Web Application

Core principles:
- Spec-driven development as the single source of truth
- Zero manual coding by the user
- Deterministic, reviewable agentic workflow
- Secure-by-default full-stack architecture
- Clear separation of concerns (frontend, backend, database, auth)

Development discipline:
- Specs must be written or updated before implementation
- Claude Code must always reference specs using @specs/... paths
- If a requirement is unclear or missing, update or create a spec before coding
- Implementation must strictly follow Spec-Kit Plus conventions
- CLAUDE.md files override default assumptions at all levels

Scope enforcement:
- Only Phase II features may be implemented
- No Phase III (AI chatbot), Phase IV (Kubernetes), or Phase V (Cloud/Kafka) work
- No mobile apps, realtime sync, payments, or RBAC
- REST API endpoints must remain exactly as specified

Architecture standards:
- Monorepo structure is mandatory
- Frontend: Next.js 16+ App Router
- Backend: Python FastAPI
- ORM: SQLModel only
- Database: Neon Serverless PostgreSQL only
- Frontend must never access the database directly
- Backend must never trust client-provided identity data

Authentication & security standards:
- Authentication handled via Better Auth on frontend
- JWT tokens are the only authentication mechanism
- JWT must be sent via Authorization: Bearer <token> header
- FastAPI must verify JWT using shared secret
- Shared secret must come from BETTER_AUTH_SECRET environment variable
- User identity must be extracted from JWT, never trusted from request body or URL
- All API endpoints require valid JWT authentication
- Requests without valid JWT must return 401 Unauthorized
- Task ownership must be enforced on every CRUD operation

API standards:
- All routes must be under /api/
- Endpoints must match the provided REST specification exactly
- Responses must be JSON
- Use Pydantic models for request and response schemas
- Proper HTTP status codes must be returned (200, 201, 400, 401, 403, 404)
- API behavior must filter all data by authenticated user only

Frontend standards:
- Server components by default
- Client components only when required for interactivity
- All API calls must go through a centralized API client
- JWT must be attached automatically to every request
- Tailwind CSS only (no inline styles)
- UI must be responsive and usable on mobile and desktop
- Authentication state managed via Better Auth session

Backend standards:
- FastAPI application entry via main.py
- SQLModel used for all database interactions
- No raw SQL unless explicitly specified in specs
- Database connection via DATABASE_URL environment variable
- Auth verification implemented via middleware or dependencies
- Errors handled with HTTPException, no stack traces exposed

Database standards:
- Schema must match @specs/database/schema.md
- tasks table must reference user_id
- Foreign key constraints must be enforced
- Indexes must exist for user_id and completed status
- No in-memory or SQLite database usage

Workflow enforcement:
1. Read relevant spec(s)
2. Generate an implementation plan
3. Break plan into small, verifiable tasks
4. Implement tasks incrementally via Claude Code
5. Validate behavior against acceptance criteria
6. Update specs if behavior changes

Disallowed actions:
- Writing code without referencing specs
- Skipping authentication or authorization checks
- Hardcoding secrets or credentials
- Mixing frontend and backend responsibilities
- Implementing undocumented behavior
- Bypassing Spec-Kit Plus structure

Success criteria:
- Full-stack application runs locally
- Multi-user authentication works correctly
- Users can only access their own tasks
- REST API is fully secured with JWT
- Neon PostgreSQL stores data persistently
- Codebase follows Spec-Kit and CLAUDE.md rules
- Project is reviewable, reproducible, and hackathon-ready
```

## Response snapshot

Constitution file created at `.specify/memory/constitution.md` with the following key sections:

- Core Principles: Spec-driven development, Zero manual coding, Deterministic workflows, Secure-by-default architecture, Clear separation of concerns, Human-in-the-loop validation
- Development Discipline: Specs-first approach, Claude Code referencing, Spec-Kit conventions
- Scope Enforcement: Phase II only, no advanced features beyond scope
- Architecture Standards: Monorepo, Next.js, FastAPI, SQLModel, Neon PostgreSQL
- Authentication & Security Standards: Better Auth, JWT, shared secrets, 401 unauthorized
- API, Frontend, Backend, Database Standards: Detailed technical requirements
- Workflow Enforcement: 6-step implementation process
- Disallowed Actions: Prevention of bad practices
- Success Criteria: Clear measurable outcomes

## Outcome

- ✅ Impact: Created project constitution with comprehensive principles and standards
- 🧪 Tests: none
- 📁 Files: 1 file created (.specify/memory/constitution.md)
- 🔁 Next prompts: Ready to proceed with spec creation and implementation
- 🧠 Reflection: Constitution provides clear guidance for all development activities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create feature specifications