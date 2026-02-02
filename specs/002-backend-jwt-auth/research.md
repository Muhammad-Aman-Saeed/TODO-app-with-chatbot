# Research Findings: Backend JWT Authentication Implementation

## Decision: JWT Claim Structure for User Identification
**Rationale**: Based on the specification, Better Auth typically places user ID in either the 'sub' claim or 'user.id' field. According to industry standards and OAuth 2.0 specifications, the 'sub' (subject) claim is the standard location for identifying the principal (user) that the token refers to. We'll implement our JWT verification to first check for 'sub' claim and fall back to other possible user ID fields if needed.
**Alternatives considered**: 
- Using a custom claim name (but this would require configuration changes)
- Storing user ID in multiple claims (unnecessary duplication)

## Decision: Database Connection Pooling for Neon PostgreSQL
**Rationale**: Neon Serverless PostgreSQL is designed for variable workloads and offers automatic scaling. For connection pooling, we'll rely on SQLModel's underlying SQLAlchemy engine configuration, which provides robust connection pooling mechanisms. We'll use the default settings initially and monitor performance to adjust pool size if needed.
**Alternatives considered**:
- Using a separate connection pooling service (overkill for this project)
- Managing connections manually (error-prone and unnecessary)

## Decision: Error Response Format Consistency
**Rationale**: To maintain API consistency and ease of frontend integration, all error responses will follow the same structure with a 'detail' field containing the error message. This aligns with FastAPI's default error handling while providing clear, actionable feedback to clients.
**Alternatives considered**:
- Different error formats for different error types (would complicate frontend handling)
- Raw exception messages (not user-friendly)

## Decision: Task Ownership Validation Approach
**Rationale**: To ensure security and prevent users from accessing other users' tasks, we'll implement ownership validation at the database query level by always filtering with `task.user_id == current_user_id`. This provides a strong security boundary that cannot be bypassed even if other validation layers fail.
**Alternatives considered**:
- Checking ownership after retrieving data (less secure)
- Using middleware for ownership validation (would be more complex and harder to maintain)

## Decision: JWT Secret Storage
**Rationale**: The specification provides a fixed BETTER_AUTH_SECRET value that must be used. We'll store this in environment variables and access it through Python's os.getenv() function, ensuring it's never hardcoded in the source code. This maintains security while meeting the requirement.
**Alternatives considered**:
- Hardcoding the secret in source (highly insecure)
- Using a more complex secret management system (unnecessary for this project)