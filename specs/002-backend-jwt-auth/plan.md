# Implementation Plan: Backend JWT Authentication Implementation

**Feature**: 002-backend-jwt-auth
**Date**: 2026-02-01
**Status**: Draft

## 1. Overall Goals & Success Criteria

### Goals
- Create a secure, production-ready FastAPI backend with JWT authentication
- Integrate seamlessly with the frontend's Better Auth JWT system
- Ensure strict user isolation - users can only access their own tasks
- Implement all required CRUD operations with proper authentication and authorization

### Success Criteria
- All API endpoints properly validate JWT tokens and enforce user ownership
- Response times under 500ms for all operations
- Proper error handling with appropriate HTTP status codes (401, 403, 404)
- Complete integration with frontend JWT flow
- Production-ready code with logging and proper error handling

## 2. Folder Structure Plan

```
/backend/
├── main.py                 # FastAPI app initialization and configuration
├── models.py               # SQLModel database models (Task model)
├── schemas.py              # Pydantic schemas for request/response validation
├── db.py                   # Database engine and session configuration
├── dependencies.py         # Dependency injection functions (get_db, get_current_user)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables template
├── .gitignore              # Git ignore rules for backend
├── README.md               # Backend documentation
├── routes/
│   └── tasks.py            # Task-related API routes
└── utils/
    └── jwt.py              # JWT verification utilities
```

## 3. Dependencies & Setup (Phase 1)

### Required Packages
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlmodel==0.0.16
- psycopg2-binary==2.9.9
- pyjwt==2.8.0
- python-dotenv==1.0.0
- pydantic==2.5.0
- python-multipart==0.0.9
- cryptography==41.0.8
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- email-validator==2.1.0

### Environment Variables
- DATABASE_URL: PostgreSQL connection string for Neon
- BETTER_AUTH_SECRET: "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5" (fixed value)

## 4. Phased Implementation Steps

### Phase 1: Base Project Setup
- **Goal**: Initialize FastAPI project with basic configuration
- **Files**: main.py, requirements.txt, .env, .gitignore
- **Tasks**:
  - Create FastAPI app instance
  - Configure CORS for localhost:3000
  - Set up basic logging
  - Install dependencies
- **Dependencies**: None
- **Complexity**: Low

### Phase 2: Database Configuration
- **Goal**: Set up database connection and session management
- **Files**: db.py
- **Tasks**:
  - Create database engine using DATABASE_URL
  - Define SessionLocal for dependency injection
  - Add alembic for migrations (future-proofing)
- **Dependencies**: Phase 1
- **Complexity**: Medium

### Phase 3: Database Models
- **Goal**: Create SQLModel models for the application
- **Files**: models.py
- **Tasks**:
  - Define Task model with user_id foreign key
  - Add required fields (title, description, completed, user_id)
  - Implement proper indexing for performance
- **Dependencies**: Phase 2
- **Complexity**: Medium

### Phase 4: Pydantic Schemas
- **Goal**: Create request/response validation schemas
- **Files**: schemas.py
- **Tasks**:
  - Define TaskCreate schema (title required, description optional)
  - Define TaskRead schema (includes ID and all fields)
  - Define TaskUpdate schema (optional fields for partial updates)
  - Define TaskPatch schema for completion toggling
- **Dependencies**: Phase 3
- **Complexity**: Low

### Phase 5: JWT Utilities & Authentication
- **Goal**: Implement JWT verification and authentication dependency
- **Files**: utils/jwt.py, dependencies.py
- **Tasks**:
  - Create verify_token function to decode and validate JWT
  - Handle token expiration and invalid signature errors
  - Create get_current_user dependency that extracts user_id from token
  - Return proper HTTP exceptions (401/403) for invalid tokens
- **Dependencies**: Phase 1
- **Complexity**: High

### Phase 6: Task Router & Endpoints
- **Goal**: Implement all task-related API endpoints with authentication
- **Files**: routes/tasks.py
- **Tasks**:
  - GET /api/tasks: List tasks with filtering (status) and sorting (created/title)
  - POST /api/tasks: Create new task with current user_id
  - GET /api/tasks/{id}: Get single task (owned by current user)
  - PUT /api/tasks/{id}: Update task (owned by current user)
  - DELETE /api/tasks/{id}: Delete task (owned by current user)
  - PATCH /api/tasks/{id}/complete: Toggle completion status (owned by current user)
  - Apply get_current_user dependency to all endpoints
  - Implement proper ownership checks (task.user_id == current_user_id)
- **Dependencies**: Phases 2, 3, 4, 5
- **Complexity**: High

### Phase 7: Main App Assembly
- **Goal**: Integrate all components into the main application
- **Files**: main.py
- **Tasks**:
  - Include task router with prefix
  - Add exception handlers
  - Configure middleware
  - Set up startup/shutdown events for database
- **Dependencies**: All previous phases
- **Complexity**: Medium

### Phase 8: Polish & Production Hardening
- **Goal**: Add production-ready features and finalize implementation
- **Files**: All files as needed
- **Tasks**:
  - Add comprehensive logging
  - Implement proper error responses
  - Add API documentation customization
  - Add health check endpoint
  - Performance optimizations
  - Security headers
- **Dependencies**: All previous phases
- **Complexity**: Medium

## 5. Security & JWT Flow Plan

### JWT Verification Process
1. Extract JWT token from Authorization header (Bearer scheme)
2. Decode token using PyJWT with HS256 algorithm
3. Verify signature using BETTER_AUTH_SECRET
4. Validate token expiration (exp) and issued-at (iat) claims
5. Extract user_id from 'sub' claim (or 'user.id' if available)
6. Return user_id or raise HTTPException with appropriate status code

### Error Handling Strategy
- Invalid signature → HTTPException(401, "Invalid token")
- Expired token → HTTPException(401, "Token expired")
- Missing user_id in payload → HTTPException(401, "Invalid token")
- User trying to access others' resources → HTTPException(403, "Access forbidden")

### Ownership Enforcement
- All endpoints retrieve current user_id via get_current_user dependency
- Before any operation, verify task.user_id == current_user_id
- Return 403 or 404 if ownership doesn't match (avoiding information disclosure)

### Frontend Integration
- Frontend sends Authorization: Bearer <token> header
- Backend validates token and extracts user_id
- All operations filtered by user_id to ensure data isolation

## 6. Risks, Assumptions & Open Questions

### Assumptions
- Better Auth JWT payload contains user_id in 'sub' claim
- Database connection to Neon PostgreSQL is stable
- Frontend will properly send JWT tokens in Authorization header

### Potential Risks
- Token expiration handling: Need to consider refresh token strategy
- Neon connection pooling: May need to configure properly for production
- Security vulnerabilities: Ensure proper validation of all inputs

### Open Questions
- What is the exact claim name for user_id in Better Auth JWTs? (sub vs user.id)
- Should we implement token refresh functionality?
- Are there any specific rate limiting requirements?

## 7. Next Action Recommendation

Start with Phase 1: Base Project Setup to establish the foundation. Create the main.py file with basic FastAPI configuration and CORS middleware for localhost:3000. Then proceed with Phase 2 to set up database connectivity.

For testing during development:
- Run with: `uvicorn main:app --reload --port 8000`
- Test endpoints with curl or Postman, providing a valid JWT in the Authorization header