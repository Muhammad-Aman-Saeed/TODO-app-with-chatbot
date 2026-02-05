---
id: 2
title: Create AI Chatbot Integration Spec
stage: spec
date_iso: 2026-02-04
surface: agent
model: Qwen
feature: ai-chatbot-integration
branch: 003-ai-chatbot-integration
user: user
command: /sp.specify
labels:
  - specification
  - ai
  - chatbot
  - todo
links:
  spec: specs/003-ai-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/003-ai-chatbot-integration/spec.md
  - specs/003-ai-chatbot-integration/checklists/requirements.md
tests_yaml: []
---

# Create AI Chatbot Integration Spec

## User Input

```
You are implementing Phase III: AI Todo Chatbot for the hackathon-todo monorepo project. PROJECT CONTEXT (Phase II already exists – integrate INSIDE it, do NOT break or rewrite existing code): - Monorepo: hackathon-todo/ - /backend: FastAPI + SQLModel + Neon PostgreSQL + Better Auth JWT - Existing: Task model, task CRUD endpoints (/api/tasks, /api/tasks/{id}, etc.) - Existing: JWT auth dependency → get_current_user() returns user_id (str) - Existing: Ownership enforced on every task operation - /frontend: Next.js 16+ App Router with Tailwind, Better Auth, task dashboard PHASE III GOAL: Build a natural-language AI chatbot that can: - Add, list, complete, delete, update tasks using conversation - Show user's own tasks only (via user_id from JWT) - Tell user about their own profile (email, name if available from Better Auth) - Maintain conversation history in DB (stateless server) - Use Cohere API as the only LLM (no OpenAI) TECHNOLOGY & INTEGRATION RULES (strict): - LLM: Cohere (cohere-py client) - Use COHERE_API_KEY from .env - Preferred model: command-r-plus (or command-a if rate limits issue) - Use Cohere's native tool use / function calling feature - Tools: Define exactly 5 Cohere-compatible tools (JSON schema format): 1. add_task(user_id: str, title: str, description: str | None = None) → returns {"task_id": int, "status": "created", "title": str} 2. list_tasks(user_id: str, status: str = "all") # "all" | "pending" | "completed" → returns list of {"id": int, "title": str, "description": str | None, "completed": bool} 3. complete_task(user_id: str, task_id: int) → returns {"task_id": int, "status": "completed", "title": str} 4. delete_task(user_id: str, task_id: int) → returns {"task_id": int, "status": "deleted", "title": str} 5. get_user_info(user_id: str) → returns {"email": str, "name": str | None} (from Better Auth user table or session) - All tools MUST: - Run inside authenticated context → validate user_id == current_user_id - Use existing SQLModel Task operations (reuse Phase II logic) - Raise exceptions on not found / permission denied → agent will catch and respond - New DB models (add to models.py): - Conversation(id: int PK, user_id: str, title: str | None, created_at, updated_at) - Message(id: int PK, conversation_id: int FK, role: Literal["user", "assistant"], content: str, created_at) - Chat Endpoint: - POST /api/chat - Authentication: JWT required (use existing get_current_user dependency) - Request body: {"message": str, "conversation_id": int | null} - Response: {"conversation_id": int, "response": str, "tool_calls": list | null} - Stateless flow in endpoint: 1. Get current_user_id from JWT 2. Get or create Conversation (if no conversation_id → create new) 3. Save user message to Message table 4. Load last 20–30 messages (ordered by created_at) → format as Cohere chat history 5. Call cohere.chat( model="command-r-plus", message=latest user message, chat_history=previous messages, tools=tool_definitions, tool_results=execute if called ) 6. Handle tool calls → execute → feed tool results back to Cohere (multi-turn if needed) 7. Get final assistant message → save to Message table 8. Return response - System prompt for Cohere (must include): "You are a friendly, helpful Todo assistant. Use the provided tools to manage the user's tasks. Always validate actions for the current user only. Confirm every action politely. Be concise, natural, and encouraging. If asked about the user, use get_user_info tool. Respond in the same language as the user if possible." FRONTEND INTEGRATION: - Add a floating chatbot icon in dashboard (bottom-right, fixed position) - Icon: chat bubble (lucide-react MessageCircle icon recommended) - On click → open modal or slide-in chat panel (use shadcn/ui Dialog or custom) - Chat UI inside modal/panel: - Message bubbles (user right, assistant left) - Input box + send button - Loading indicator when processing - Auto-scroll to bottom - Show previous messages on open (fetch via conversation_id) - API call: use existing /lib/api.ts → add chat(message, conversation_id?) - Attach Authorization: Bearer <token> - Store conversation_id in localStorage or state for continuity OUTPUT FORMAT (implement step-by-step): 1. Show updated /backend folder structure additions only 2. List new pip packages needed: - cohere - (others if any) 3. Show complete code for: - New models additions (models.py) - Tool definitions (schemas or tools.py) - Tool execution functions (services/task_service.py or similar) - POST /api/chat endpoint (routes/chat.py or in main router) - Cohere client initialization & chat logic 4. Show frontend additions: - New component: ChatbotModal.tsx or ChatPanel.tsx - Dashboard layout update → add floating icon + modal trigger - api.ts update → add chat() function 5. .env update instruction: add COHERE_API_KEY=... 6. Make UI beautiful: Tailwind gradients, smooth animations, dark mode compatible Implement now – start with backend additions (models → tools → endpoint → Cohere integration), then frontend chatbot UI.
```

## Response Summary

Created a comprehensive feature specification for the AI Todo Chatbot Integration. The specification includes:

1. User stories covering natural language task management (P1), persistent conversation history (P2), and user profile information access (P3)
2. Functional requirements covering authentication, task management, conversation storage, and error handling
3. Key entities (Conversation, Message, Task) with clear definitions
4. Success criteria with measurable outcomes for task completion rates, response times, and reliability

The specification follows the template structure and focuses on user value without implementation details. A quality checklist was also created to validate the specification completeness.

## Outcome

Successfully created a detailed feature specification that captures all requirements for the AI Todo Chatbot integration. The specification is ready for the planning phase and includes all necessary information to guide the development process.