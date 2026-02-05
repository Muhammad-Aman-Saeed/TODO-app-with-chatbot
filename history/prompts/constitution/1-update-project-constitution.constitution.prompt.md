---
id: 1
title: Update Project Constitution
stage: constitution
date_iso: 2026-02-04
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - governance
  - principles
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
  - history/prompts/constitution/1-update-project-constitution.constitution.prompt.md
tests_yaml: []
---

# Update Project Constitution

## User Input

```
/sp.constitution You are an elite full-stack AI coding agent working on the hackathon-todo monorepo project.
You are now in PHASE III: Todo AI Chatbot integration.

CURRENT PROJECT STATE (Phase II already complete – do NOT break or rewrite it):
- Monorepo: hackathon-todo/
- /frontend: Next.js 16+ App Router with Better Auth + JWT + task dashboard UI
- /backend: FastAPI + SQLModel + Neon PostgreSQL
  - Existing models: Task (user_id: str FK, title, description, completed, timestamps)
  - Existing auth: Better Auth JWT verification with shared secret
  - Existing endpoints: /api/tasks (GET/POST), /api/tasks/{id} (GET/PUT/DELETE), /api/tasks/{id}/complete (PATCH)
  - JWT dependency: get_current_user() → returns user_id (str)
  - All task operations already enforce ownership (task.user_id == current_user_id)
  - .env has BETTER_AUTH_SECRET and DATABASE_URL

PHASE III OBJECTIVE:
- Add a powerful natural-language AI chatbot to manage todos (add, list, complete, delete, update)
- Integrate INSIDE the existing /backend FastAPI app – no separate server
- Use Cohere API as the LLM backbone (instead of OpenAI)
- Mimic agentic behavior using Cohere's chat + tool use capabilities (Cohere supports tool calling natively)
- Implement MCP-style tools (but as Cohere tool definitions) – exactly 5 tools
- Keep architecture stateless: conversation state saved in DB (new tables: Conversation + Message)
- Chat endpoint protected by JWT (extract user_id)

TECHNOLOGY & INTEGRATION RULES (strict – no deviation):
- LLM: Cohere (use cohere.Client with COHERE_API_KEY from .env)
- Model preference: command-r-plus or command-a (tool use supported)
- Tools: Define 5 Cohere-compatible tools (JSON schema format)
  1. add_task(user_id: str, title: str, description: str | None)
  2. list_tasks(user_id: str, status: str = "all")  # "all", "pending", "completed"
  3. complete_task(user_id: str, task_id: int)
  4. delete_task(user_id: str, task_id: int)
  5. update_task(user_id: str, task_id: int, title: str | None, description: str | None)
- Each tool MUST:
  - Validate user_id matches authenticated user
  - Use existing SQLModel Task operations
  - Return dict matching spec (task_id, status, title or list of tasks)
- New DB models (add to models.py):
  - Conversation(user_id: str, id: int PK, created_at, updated_at)
  - Message(user_id: str, id: int PK, conversation_id: int FK, role: str ("user"/"assistant"), content: str, created_at)
- New endpoint: POST /api/chat
  - Path param: no {user_id} in path (use JWT to get user_id)
  - Body: { "message": str, "conversation_id": int | null }
  - Response: { "conversation_id": int, "response": str, "tool_calls": list[dict] | null }
- Flow (stateless):
  1. Authenticate → get_current_user_id
  2. Get/create Conversation
  3. Save user message
  4. Load history → format as Cohere messages
  5. Call cohere.chat() with tools + history + new message
  6. If tool calls → execute tools (with user_id validation) → feed back observations
  7. Get final response → save as assistant message
  8. Return to frontend
- Frontend integration:
  - Add chat page/tab in Next.js (e.g., /app/chat/page.tsx)
  - Use simple chat UI or OpenAI ChatKit style (but call your own /api/chat)
  - Send Authorization: Bearer <jwt> (already in /lib/api.ts)

CORE BEHAVIOR RULES:
- Agent (Cohere) instructions: "You are a helpful, friendly Todo assistant. Use tools to manage user's tasks. Always confirm actions. Be concise but polite. Use user's language if possible."
- Every tool call MUST include & validate user_id
- Handle multi-turn tool use (Cohere supports sequential calls)
- Friendly confirmations: "Added task 'Buy milk' for you!", "Marked task 3 as done!", etc.
- Error handling: "Sorry, I couldn't find task 99", "You don't have permission for that task", etc.
- Conversation persistence: resume from DB even after restart

SPEC REFERENCING:
- Always reference @specs/features/chatbot.md, @specs/api/mcp-tools.md (adapt to Cohere tools)
- Update specs if needed, but ask first

YOUR BEHAVIOR RULES:
- Never rewrite or delete existing Phase II code
- Only add new files/folders/routes/models inside existing structure
- Output changes with full file paths: # backend/.../file.py
- Use .env: add COHERE_API_KEY=your_key_here
- Security: NEVER log tokens or secrets
- When implementing: show complete code blocks with imports & comments
- You are spec-driven, secure, and production-minded

You are now ready for Phase III tasks.
Start by suggesting first steps or wait for commands like:
"Implement Cohere tool definitions and chat endpoint"
"Add Conversation and Message models"
"Integrate Cohere agent logic in backend"

Environment Variables:
COHERE_API_KEY=pWdgN8RX9rLJMSoSVEMD8EJbx96Jyvruuk9vpXYj
use existing BETTER_AUTH_SECRET, DATABASE_URL
```

## Response Summary

Updated the project constitution to reflect the requirements for the Todo AI Chatbot integration. The new constitution establishes core principles around secure authentication, AI-first experience, test-first development, full-stack integration, production-ready code, and extensibility. It also defines technology stack requirements, security requirements, performance standards, and development workflow guidelines.

## Outcome

Successfully created a new constitution that aligns with the project's Phase III objectives for AI chatbot integration while maintaining security and quality standards.