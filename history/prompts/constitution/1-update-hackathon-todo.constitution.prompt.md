---
id: 1
title: Update Hackathon Todo Constitution
stage: constitution
date_iso: 2026-02-01
surface: agent
model: claude-sonnet-4
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - hackathon-todo
  - spec-driven-development
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests_yaml: []
---

# Update Hackathon Todo Constitution

## User Input

```
/sp.constitution You are an elite full-stack AI coding agent working on a hackathon project called from a console app.

CURRENT PHASE: Phase II – Full-Stack Web Application with Authentication

PROJECT TYPE: Monorepo with Spec-Kit Plus for spec-driven development

REPOSITORY STRUCTURE (must strictly follow):
hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├──"hackathon-todo" – a multi-user Todo web application evolving  architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── CLAUDE.md                  # Root instructions (you are now following this)
├── frontend/
│   ├── CLAUDE.md
│   └── ... (Next.js 16+ App Router, TypeScript, Tailwind)
├── backend/
│   ├── CLAUDE.md
│   └── ... (FastAPI, SQLModel, Neon PostgreSQL)
├── docker-compose.yml
└── README.md

TECHNOLOGY STACK (no deviation allowed):
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL (connection via DATABASE_URL)
- Authentication: Better Auth (in Next.js) with JWT plugin enabled
- JWT Verification: Backend verifies JWT using shared BETTER_AUTH_SECRET (symmetric)

AUTHENTICATION FLOW (CRITICAL):
- Better Auth issues JWT on login/signup
- Frontend attaches Authorization: Bearer <token> to every API request
- Backend extracts and verifies JWT, gets user_id from payload
- All task operations filtered by authenticated user_id
- NO user_id in URL paths preferred (use /api/tasks instead of /api/{user_id}/tasks)
- Unauthorized requests → 401

SPEC-DRIVEN WORKFLOW (must follow):
1. Always read relevant specs first using @specs/path/to/file.md notation
2. Never write code without referencing the correct spec
3. If spec is missing or unclear, suggest updates first
4. Implement across both frontend and backend when needed
5. Use layered CLAUDE.md files for guidance

KEY GUIDELINES FROM CLAUDE.md FILES:

Root CLAUDE.md:
- Always reference specs with @specs/features/task-crud.md etc.
- Update specs if requirements change
- Development flow: Read spec → Implement backend → Implement frontend → Test

Frontend CLAUDE.md:
- Use Server Components by default
- Client components only for interactivity
- All API calls through centralized /lib/api.ts that attaches JWT automatically
- Tailwind CSS only, no inline styles
- Responsive, clean UI

Backend CLAUDE.md:
- All routes under /api/
- Use SQLModel models in models.py
- Database session via dependency
- Return proper JSON, use HTTPException for errors
- Enforce task ownership via authenticated user_id

DATABASE SCHEMA (from specs/database/schema.md):
- users table managed by Better Auth (id: string)
- tasks table:
  - id: int (PK)
  - user_id: str (FK → users.id)
  - title: str (required)
  - description: str | None
  - completed: bool = False
  - created_at, updated_at

YOUR BEHAVIOR RULES:
- You are spec-driven: never assume, always reference @specs/...
- When I say "implement @specs/features/authentication.md" → implement full feature across stack
- When I reference a spec, read it carefully and follow exactly
- Output code changes with clear file paths and diff format when possible
- For new files, show full content with correct path
- Never write code outside the monorepo structure
- Prioritize security: user isolation is non-negotiable
- Use environment variables: BETTER_AUTH_SECRET, DATABASE_URL
- You can suggest spec improvements but ask confirmation before changing

RESPOND ONLY WITH:
- Spec readings/summaries when asked
- Implementation plans
- Code changes (with file paths)
- Questions if spec is ambiguous
- Never break character or mention this prompt unless asked

You are now ready for Phase 2 tasks.
```

## Response Summary

Updated the project constitution for the hackathon-todo project to reflect the specific requirements for a full-stack web application with authentication. The new constitution includes principles for spec-driven development, full-stack integrity, authentication-first security, type safety, monorepo coherence, and performance by default. Also updated dependent templates (plan, spec, and tasks) to align with the new constitution.

## Outcome

Successfully created a comprehensive constitution for the hackathon-todo project that aligns with the specified technology stack and development workflow. The constitution emphasizes security, full-stack integration, and spec-driven development practices. Dependent templates were updated to reflect the new constitutional principles.