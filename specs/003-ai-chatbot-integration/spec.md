# Feature Specification: AI Todo Chatbot Integration

**Feature Branch**: `003-ai-chatbot-integration`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "You are implementing Phase III: AI Todo Chatbot for the hackathon-todo monorepo project. PROJECT CONTEXT (Phase II already exists – integrate INSIDE it, do NOT break or rewrite existing code): - Monorepo: hackathon-todo/ - /backend: FastAPI + SQLModel + Neon PostgreSQL + Better Auth JWT - Existing: Task model, task CRUD endpoints (/api/tasks, /api/tasks/{id}, etc.) - Existing: JWT auth dependency → get_current_user() returns user_id (str) - Existing: Ownership enforced on every task operation - /frontend: Next.js 16+ App Router with Tailwind, Better Auth, task dashboard PHASE III GOAL: Build a natural-language AI chatbot that can: - Add, list, complete, delete, update tasks using conversation - Show user's own tasks only (via user_id from JWT) - Tell user about their own profile (email, name if available from Better Auth) - Maintain conversation history in DB (stateless server) - Use Cohere API as the only LLM (no OpenAI) TECHNOLOGY & INTEGRATION RULES (strict): - LLM: Cohere (cohere-py client) - Use COHERE_API_KEY from .env - Preferred model: command-r-plus (or command-a if rate limits issue) - Use Cohere's native tool use / function calling feature - Tools: Define exactly 5 Cohere-compatible tools (JSON schema format): 1. add_task(user_id: str, title: str, description: str | None = None) → returns {"task_id": int, "status": "created", "title": str} 2. list_tasks(user_id: str, status: str = "all") # "all" | "pending" | "completed" → returns list of {"id": int, "title": str, "description": str | None, "completed": bool} 3. complete_task(user_id: str, task_id: int) → returns {"task_id": int, "status": "completed", "title": str} 4. delete_task(user_id: str, task_id: int) → returns {"task_id": int, "status": "deleted", "title": str} 5. get_user_info(user_id: str) → returns {"email": str, "name": str | None} (from Better Auth user table or session) - All tools MUST: - Run inside authenticated context → validate user_id == current_user_id - Use existing SQLModel Task operations (reuse Phase II logic) - Raise exceptions on not found / permission denied → agent will catch and respond - New DB models (add to models.py): - Conversation(id: int PK, user_id: str, title: str | None, created_at, updated_at) - Message(id: int PK, conversation_id: int FK, role: Literal["user", "assistant"], content: str, created_at) - Chat Endpoint: - POST /api/chat - Authentication: JWT required (use existing get_current_user dependency) - Request body: {"message": str, "conversation_id": int | null} - Response: {"conversation_id": int, "response": str, "tool_calls": list | null} - Stateless flow in endpoint: 1. Get current_user_id from JWT 2. Get or create Conversation (if no conversation_id → create new) 3. Save user message to Message table 4. Load last 20–30 messages (ordered by created_at) → format as Cohere chat history 5. Call cohere.chat( model="command-r-plus", message=latest user message, chat_history=previous messages, tools=tool_definitions, tool_results=execute if called ) 6. Handle tool calls → execute → feed tool results back to Cohere (multi-turn if needed) 7. Get final assistant message → save to Message table 8. Return response - System prompt for Cohere (must include): "You are a friendly, helpful Todo assistant. Use the provided tools to manage the user's tasks. Always validate actions for the current user only. Confirm every action politely. Be concise, natural, and encouraging. If asked about the user, use get_user_info tool. Respond in the same language as the user if possible." FRONTEND INTEGRATION: - Add a floating chatbot icon in dashboard (bottom-right, fixed position) - Icon: chat bubble (lucide-react MessageCircle icon recommended) - On click → open modal or slide-in chat panel (use shadcn/ui Dialog or custom) - Chat UI inside modal/panel: - Message bubbles (user right, assistant left) - Input box + send button - Loading indicator when processing - Auto-scroll to bottom - Show previous messages on open (fetch via conversation_id) - API call: use existing /lib/api.ts → add chat(message, conversation_id?) - Attach Authorization: Bearer <token> - Store conversation_id in localStorage or state for continuity OUTPUT FORMAT (implement step-by-step): 1. Show updated /backend folder structure additions only 2. List new pip packages needed: - cohere - (others if any) 3. Show complete code for: - New models additions (models.py) - Tool definitions (schemas or tools.py) - Tool execution functions (services/task_service.py or similar) - POST /api/chat endpoint (routes/chat.py or in main router) - Cohere client initialization & chat logic 4. Show frontend additions: - New component: ChatbotModal.tsx or ChatPanel.tsx - Dashboard layout update → add floating icon + modal trigger - api.ts update → add chat() function 5. .env update instruction: add COHERE_API_KEY=... 6. Make UI beautiful: Tailwind gradients, smooth animations, dark mode compatible Implement now – start with backend additions (models → tools → endpoint → Cohere integration), then frontend chatbot UI."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Management (Priority: P1)

As a user, I want to interact with my todo list using natural language so that I can manage my tasks more efficiently without navigating through multiple UI elements.

**Why this priority**: This is the core functionality of the AI chatbot and provides the primary value proposition of the feature.

**Independent Test**: The user can add, list, complete, delete, and update tasks using natural language commands like "Add a task to buy groceries" or "Show me my pending tasks" and receive appropriate responses.

**Acceptance Scenarios**:

1. **Given** user is authenticated and on the dashboard, **When** user types "Add a task to buy groceries", **Then** a new task titled "buy groceries" is created and the user receives confirmation
2. **Given** user has multiple tasks, **When** user types "Show me my pending tasks", **Then** the user sees a list of all incomplete tasks
3. **Given** user has pending tasks, **When** user types "Complete task 1", **Then** task 1 is marked as completed and the user receives confirmation

---

### User Story 2 - Persistent Conversation History (Priority: P2)

As a user, I want my conversations with the AI chatbot to be saved so that I can continue my task management conversations across sessions.

**Why this priority**: This enhances user experience by allowing continuity in conversations and provides context for the AI to better assist the user.

**Independent Test**: When a user returns to the application, they can view their previous conversations with the chatbot and continue from where they left off.

**Acceptance Scenarios**:

1. **Given** user has had previous conversations with the chatbot, **When** user opens the chat interface, **Then** they can see their previous conversation history
2. **Given** user closes the application after chatting with the bot, **When** user returns to the application, **Then** their conversation history is preserved

---

### User Story 3 - User Profile Information Access (Priority: P3)

As a user, I want to ask the AI chatbot about my profile information so that I can verify my identity or get account details through the chat interface.

**Why this priority**: This provides a convenient way for users to access their account information without leaving the chat interface.

**Independent Test**: When a user asks the chatbot for their profile information (e.g., "What is my email?"), the system retrieves and displays the user's email and name from their account.

**Acceptance Scenarios**:

1. **Given** user is authenticated, **When** user asks "What is my email?", **Then** the chatbot responds with the user's email address
2. **Given** user is authenticated, **When** user asks "Tell me about myself", **Then** the chatbot responds with the user's name and email

---

### Edge Cases

- What happens when the AI service is temporarily unavailable?
- How does the system handle malformed natural language requests?
- What occurs when a user attempts to access another user's tasks?
- How does the system handle requests for non-existent tasks?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate all chat requests using existing JWT mechanism
- **FR-002**: System MUST ensure users can only access their own tasks and conversations
- **FR-003**: Users MUST be able to add tasks using natural language through the chat interface
- **FR-004**: Users MUST be able to list tasks (all, pending, or completed) using natural language
- **FR-005**: Users MUST be able to complete, delete, and update tasks using natural language
- **FR-006**: System MUST store conversation history in the database with proper associations to users
- **FR-007**: System MUST integrate with Cohere API for natural language processing and tool calling
- **FR-008**: System MUST provide user profile information (email, name) when requested
- **FR-009**: System MUST validate all user IDs match the authenticated user before executing operations
- **FR-010**: System MUST handle errors gracefully and provide informative responses to users

### Key Entities

- **Conversation**: Represents a chat session between a user and the AI assistant, containing metadata like creation time and user association
- **Message**: Represents individual messages within a conversation, including content, sender (user/assistant), and timestamp
- **Task**: Represents user tasks with title, description, completion status, and user ownership

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully add, list, complete, delete, and update tasks using natural language in 95% of attempts
- **SC-002**: Chat responses are delivered within 5 seconds for 90% of requests
- **SC-003**: Users can access their conversation history across sessions with 99% reliability
- **SC-004**: Zero incidents of users accessing other users' tasks or conversations occur during testing
- **SC-005**: 85% of users report that the AI chatbot improves their task management efficiency
