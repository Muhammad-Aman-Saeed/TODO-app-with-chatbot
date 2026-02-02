# Feature Specification: Backend JWT Authentication Implementation

**Feature Branch**: `002-backend-jwt-auth`
**Created**: 2026-02-01
**Status**: Draft
**Input**: User description: "You are implementing the backend for the hackathon-todo Phase 2 full-stack application in a monorepo. PROJECT: Monorepo at hackathon-todo/ CURRENT TASK: Create the complete /backend folder with a secure, production-ready FastAPI application integrated with frontend via JWT. REQUIREMENTS (strictly follow the hackathon document): - Use FastAPI latest version - SQLModel as ORM (SQLModel models with table=True) - Database: Neon Serverless PostgreSQL – connection string from env var DATABASE_URL - Authentication: Better Auth JWT integration - Frontend uses Better Auth (in Next.js) with JWT plugin enabled - Better Auth issues JWT tokens (via /api/auth/token or client plugin) - Backend verifies JWT using the shared secret: BETTER_AUTH_SECRET = "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5" - Use PyJWT library to decode and verify HS256 signed tokens - Extract user_id (string) from JWT payload (Better Auth typically puts sub or user.id in payload) - Create dependency: get_current_user() → returns user_id or raises 401/403 - All task endpoints MUST filter by authenticated user_id (task.user_id == current_user_id) - Unauthorized → 401 Unauthorized - Wrong user trying to access others' tasks → 403 Forbidden or 404 - API Endpoints (base /api/ – prefer no {user_id} in path as per modern practice, but follow document if needed): - GET /api/tasks → list all tasks for current user (query params: status=all|pending|completed, sort=created|title) - POST /api/tasks → create new task (body: title required, description optional) - GET /api/tasks/{id} → get single task (only if owned) - PUT /api/tasks/{id} → update task (only owned) - DELETE /api/tasks/{id} → delete task (only owned) - PATCH /api/tasks/{id}/complete → toggle completed status (only owned) - Use Pydantic models for request/response bodies - Return JSON, use HTTPException for errors - Project Structure (follow /backend/CLAUDE.md): - main.py → FastAPI app = FastAPI(), include routers - models.py → SQLModel classes: Task (with user_id: str = Field(foreign_key="users.id")) - schemas.py → Pydantic models: TaskCreate, TaskRead, TaskUpdate - routes/tasks.py → APIRouter(prefix="/tasks"), all endpoints with dependency on get_current_user - dependencies.py → get_db() session dependency, get_current_user() JWT verifier - db.py → engine = create_engine(DATABASE_URL), SessionLocal - utils/jwt.py → verify_token(token: str) → returns payload or raises - Security: - Use PyJWT for verification: jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"]) - Validate: exp, iat, sub/user_id present - No session table needed – stateless JWT - Other: - CORS: allow frontend origin[](http://localhost:3000) - Uvicorn running: uvicorn main:app --reload --port 8000 - Follow specs: @specs/api/rest-endpoints.md, @specs/database/schema.md, @specs/features/task-crud.md, @specs/features/authentication.md - Users table managed by Better Auth (no need to define in SQLModel, but reference user_id as str FK) OUTPUT FORMAT: 1. First, show the full /backend folder structure with all files backend/ ├── main.py ├── models.py ├── schemas.py ├── routes/ │ └── tasks.py ├── dependencies.py ├── db.py ├── utils/ │ └── jwt.py ├── requirements.txt (or pyproject.toml if using poetry/uv) └── CLAUDE.md (if needed, but already exists) 2. List required pip packages: - fastapi - uvicorn - sqlmodel - psycopg2-binary (for Neon Postgres) - pyjwt - python-dotenv (for env) - pydantic 3. Show complete code for EVERY key file with exact path: - Use ```python\n# backend/main.py\ncode here - Include imports, comments, error handling 4. JWT Verification Implementation: - In dependencies.py or utils/jwt.py: function to decode token using the exact BETTER_AUTH_SECRET provided - Handle common errors: InvalidSignatureError, ExpiredSignatureError → raise HTTPException(401/403) 5. Ensure full integration with frontend: - Frontend sends Authorization: Bearer <jwt-token> (from Better Auth) - Backend verifies it and filters tasks by extracted user_id - No shared DB session needed – pure JWT stateless 6. Make it production-ready: add basic logging, proper status codes, response models Implement now – start with folder structure, then dependencies, then core files (db, models, jwt utils, dependencies, routes, main)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

As an authenticated user, I want to securely manage my tasks through a protected API so that my personal data remains private and only accessible to me.

**Why this priority**: This is the core functionality of the application - users must be able to securely access their own tasks without exposing others' data.

**Independent Test**: Can be fully tested by authenticating with JWT, creating tasks, and verifying that only the authenticated user's tasks are accessible.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token, **When** they request their tasks via GET /api/tasks, **Then** they receive only their own tasks and not others' tasks
2. **Given** a user is authenticated with a valid JWT token, **When** they create a new task via POST /api/tasks, **Then** the task is associated with their user ID and stored securely

---

### User Story 2 - JWT Token Validation (Priority: P1)

As a system administrator, I want the backend to properly validate JWT tokens so that unauthorized users cannot access the system and data integrity is maintained.

**Why this priority**: Security is paramount - invalid or expired tokens must be rejected to prevent unauthorized access.

**Independent Test**: Can be tested by sending requests with valid tokens, expired tokens, and invalid tokens to verify proper validation.

**Acceptance Scenarios**:

1. **Given** a user presents an expired JWT token, **When** they request their tasks, **Then** the system returns a 401 Unauthorized response
2. **Given** a user presents an invalid JWT token, **When** they request their tasks, **Then** the system returns a 401 Unauthorized response

---

### User Story 3 - CRUD Operations for Tasks (Priority: P2)

As an authenticated user, I want to perform CRUD operations on my tasks so that I can manage my to-do items effectively.

**Why this priority**: This provides the essential functionality for users to interact with their tasks beyond just viewing them.

**Independent Test**: Can be tested by authenticating, creating tasks, updating them, marking as complete, and deleting them.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token, **When** they update a task via PUT /api/tasks/{id}, **Then** only their own task can be updated and others' tasks return 403/404
2. **Given** a user is authenticated with a valid JWT token, **When** they delete a task via DELETE /api/tasks/{id}, **Then** only their own task can be deleted and others' tasks return 403/404

---

### User Story 4 - Task Filtering and Sorting (Priority: P3)

As an authenticated user, I want to filter and sort my tasks so that I can efficiently navigate and manage my to-do list.

**Why this priority**: Enhances user experience by allowing better organization of tasks.

**Independent Test**: Can be tested by authenticating and requesting tasks with different filter and sort parameters.

**Acceptance Scenarios**:

1. **Given** a user has multiple tasks with different statuses, **When** they request tasks with status=pending, **Then** only pending tasks are returned
2. **Given** a user has multiple tasks, **When** they request tasks with sort=title, **Then** tasks are returned sorted by title

---

### Edge Cases

- What happens when a user attempts to access a task that doesn't exist?
- How does the system handle requests with malformed JWT tokens?
- What occurs when a user tries to access another user's task ID?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify JWT tokens using the shared secret: BETTER_AUTH_SECRET = "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5"
- **FR-002**: System MUST extract user_id from JWT payload and use it to filter task access
- **FR-003**: System MUST allow authenticated users to create tasks via POST /api/tasks
- **FR-004**: System MUST allow authenticated users to retrieve their tasks via GET /api/tasks with filtering and sorting options
- **FR-005**: System MUST allow authenticated users to update their tasks via PUT /api/tasks/{id}
- **FR-006**: System MUST allow authenticated users to delete their tasks via DELETE /api/tasks/{id}
- **FR-007**: System MUST allow authenticated users to toggle task completion via PATCH /api/tasks/{id}/complete
- **FR-008**: System MUST return 401 Unauthorized for requests with invalid/expired JWT tokens
- **FR-009**: System MUST return 403 Forbidden or 404 Not Found when users attempt to access tasks belonging to other users
- **FR-010**: System MUST store tasks in a Neon Serverless PostgreSQL database using SQLModel ORM
- **FR-011**: System MUST implement CORS to allow requests from frontend origin http://localhost:3000

### Key Entities

- **Task**: Represents a user's to-do item with properties like title, description, completion status, and association to a user
- **User**: Represents an authenticated user identified by user_id extracted from JWT token
- **JWT Token**: Secure authentication mechanism that contains user identity and expiration information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can authenticate via JWT and access only their own tasks with 99.9% accuracy
- **SC-002**: System rejects invalid or expired JWT tokens with appropriate HTTP status codes (401/403) 100% of the time
- **SC-003**: Authenticated users can perform all CRUD operations on their tasks with response times under 500ms
- **SC-004**: System prevents unauthorized access to other users' tasks 100% of the time
- **SC-005**: API endpoints handle concurrent requests from multiple users without data leakage between user accounts