# Implementation Plan: AI Todo Chatbot Integration

**Branch**: `003-ai-chatbot-integration` | **Date**: 2026-02-04 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a natural-language AI chatbot for todo management using Cohere's API with native tool calling capabilities. The system will allow users to manage their tasks through conversational interface while maintaining security through JWT authentication and user isolation. The chatbot will integrate with existing backend infrastructure and provide a seamless frontend experience via a floating chat interface.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.0+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Cohere Python SDK, Next.js 16+, Better Auth
**Storage**: Neon PostgreSQL with SQLModel ORM
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (browser-based)
**Project Type**: Web application (monorepo with separate frontend/backend)
**Performance Goals**: <5s response time for 90% of chat requests, <500ms for API operations
**Constraints**: User data isolation required, JWT authentication enforcement, Cohere API rate limits
**Scale/Scope**: Individual user task management, conversation history persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Secure Authentication & Authorization**: ✓ Verified - JWT authentication required for all chat endpoints with user_id validation
- **AI-First Experience**: ✓ Verified - Cohere API integration with natural language processing
- **Test-First (NON-NEGOTIABLE)**: ✓ Verified - Unit and integration tests required for all new functionality
- **Full-Stack Integration**: ✓ Verified - Backend API endpoints and frontend UI components
- **Production-Ready Code**: ✓ Verified - Proper error handling, logging, and security measures
- **Extensibility & Maintainability**: ✓ Verified - Modular design with clear separation of concerns

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── models.py                    # append Conversation & Message models
├── routes/
│   └── chat.py                 # new file for /api/chat endpoint
├── services/
│   └── task_service.py         # tool execution logic
├── tools/
│   └── cohere_tools.py         # tool schemas and execution functions
└── main.py                     # updated with new route inclusion

frontend/
├── components/
│   ├── ChatbotIcon.tsx         # floating chatbot icon component
│   └── ChatModal.tsx           # chat interface modal component
├── app/
│   └── dashboard/              # updated with chatbot integration
├── lib/
│   └── api.ts                  # updated with chat API method
└── styles/
    └── globals.css             # updated with chat UI styles
```

**Structure Decision**: Web application structure chosen based on existing project architecture with separate frontend and backend components.

## Overall Goals & Success Criteria

### What makes Phase III "successfully complete"?
- Users can manage their tasks using natural language through the chat interface
- Conversation history persists across sessions with proper user isolation
- Cohere AI integration works reliably with tool calling for task operations
- Frontend provides intuitive chat experience with responsive UI
- All security requirements met (user isolation, JWT authentication)

### Key integration checkpoints
- Backend: Cohere API ↔ Tool execution functions ↔ Database operations
- Frontend: Chat UI ↔ API client ↔ Backend endpoint
- Security: JWT authentication ↔ User ID validation ↔ Data access controls

### Security & UX benchmarks
- User isolation: Users can only access their own tasks and conversations
- Smooth chat experience: <5s response time for 90% of requests
- Beautiful UI: Responsive, accessible, and aesthetically pleasing chat interface

## Dependencies & Environment Setup

### New pip packages (backend)
- `cohere` - for Cohere API integration
- `python-dotenv` - for environment variable management (if not already present)

### New npm packages (frontend)
- `lucide-react` - for chatbot icon (if not already present)
- `react-markdown` - for rendering markdown responses from AI (optional)

### .env additions
- `COHERE_API_KEY` - for Cohere API access

### Migration notes
- Database migration required for Conversation and Message models
- Manual update to .env file with COHERE_API_KEY

## Phased Implementation Steps

### Phase 1: Database Extensions (Complexity: Low)
**Goal**: Add Conversation and Message models to existing models.py
**Files to create/modify**: `backend/models.py`
**Key decisions**: Define proper relationships between Conversation, Message, and existing Task/User models
**Dependencies**: None (foundational)
**Security focus**: Ensure proper user_id associations
**UX notes**: N/A (backend only)

### Phase 2: Define Cohere Tool Schemas (Complexity: Medium)
**Goal**: Create tool definitions that match Cohere's JSON schema format
**Files to create/modify**: `backend/tools/cohere_tools.py`
**Key decisions**: Define exact JSON schemas for add_task, list_tasks, complete_task, delete_task, get_user_info
**Dependencies**: Phase 1 (needs models)
**Security focus**: Include user_id validation in all tools
**UX notes**: N/A (backend only)

### Phase 3: Build Tool Service Layer (Complexity: Medium)
**Goal**: Implement service functions that execute tools with user validation
**Files to create/modify**: `backend/services/task_service.py`
**Key decisions**: Reuse existing Phase II CRUD operations with user_id validation
**Dependencies**: Phase 1 & 2 (needs models and tool schemas)
**Security focus**: Validate user_id matches authenticated user for all operations
**UX notes**: N/A (backend only)

### Phase 4: Implement POST /api/chat Endpoint (Complexity: High)
**Goal**: Create the main chat endpoint with Cohere integration
**Files to create/modify**: `backend/routes/chat.py`
**Key decisions**: Implement stateless conversation flow using DB persistence
**Dependencies**: Phase 1, 2 & 3 (needs all previous components)
**Security focus**: JWT authentication and user_id extraction
**UX notes**: N/A (backend only)

### Phase 5: Handle Tool Calls Loop (Complexity: High)
**Goal**: Implement multi-turn tool execution with result feeding back to Cohere
**Files to create/modify**: `backend/routes/chat.py` (continue)
**Key decisions**: Handle sequential tool calls and feed results back to model
**Dependencies**: Phase 4 (needs main chat endpoint)
**Security focus**: Validate each tool call against authenticated user
**UX notes**: N/A (backend only)

### Phase 6: Frontend - Add Chatbot Icon (Complexity: Low)
**Goal**: Add floating chatbot icon to dashboard UI
**Files to create/modify**: `frontend/app/dashboard/page.tsx`, `frontend/components/ChatbotIcon.tsx`
**Key decisions**: Position, styling, and animation for floating icon
**Dependencies**: None (can be developed in parallel)
**Security focus**: Ensure proper authentication context
**UX notes**: Bottom-right position, subtle animation, accessible

### Phase 7: Build Chat Modal/Panel UI (Complexity: Medium)
**Goal**: Create chat interface with message bubbles and input
**Files to create/modify**: `frontend/components/ChatModal.tsx`
**Key decisions**: Modal vs sliding panel, message display format, loading states
**Dependencies**: Phase 6 (needs trigger mechanism)
**Security focus**: Ensure JWT headers are attached to API calls
**UX notes**: Responsive design, dark mode support, smooth animations

### Phase 8: Update API Client (Complexity: Low)
**Goal**: Add chat method to existing API client
**Files to create/modify**: `frontend/lib/api.ts`
**Key decisions**: Error handling, loading states, JWT header attachment
**Dependencies**: None (can be developed in parallel)
**Security focus**: Proper JWT header inclusion
**UX notes**: Consistent with existing API client patterns

### Phase 9: Polish & Testing (Complexity: Medium)
**Goal**: Complete integration, testing, and polish
**Files to create/modify**: All components for final adjustments
**Key decisions**: Conversation persistence strategy, error messaging, accessibility
**Dependencies**: All previous phases
**Security focus**: End-to-end security validation
**UX notes**: Complete user experience validation, animations, responsive design

## UI/UX & Design System Plan (Frontend)

### Floating Icon Style
- Position: Fixed bottom-right corner with 24px margin
- Size: 60x60px circle with subtle shadow
- Color: Primary brand color with hover effect
- Animation: Gentle pulse or slide-in from corner
- Accessibility: Proper aria-label and keyboard navigation

### Chat Modal Design
- Size: 400px wide on desktop, full-width on mobile
- Background: Semi-transparent overlay with backdrop blur
- Container: White/light mode, dark gray/dark mode with rounded corners
- Shadow: Medium depth shadow for depth perception
- Header: Clean title with close button

### Message Bubble Styles
- User messages: Right-aligned, primary color background, white text
- Assistant messages: Left-aligned, light gray background, dark text
- Timestamps: Subtle, smaller font below messages
- Typography: Clear, readable fonts with appropriate sizing

### Animation Suggestions
- Modal entrance: Slide-up with fade-in
- Message appearance: Staggered fade-in
- Loading indicators: Pulse animation for AI responses
- Icon interaction: Scale transform on hover/click

### Accessibility Notes
- Keyboard navigation for all interactive elements
- Proper contrast ratios for text
- Screen reader support for messages and controls
- Focus management when modal opens

## Risks, Assumptions & Clarifications Needed

### Assumptions
- Cohere API will return consistent tool call formats
- Existing JWT authentication mechanism can be reused without modification
- Better Auth provides user information accessible for get_user_info tool

### Potential Issues
- Rate limits from Cohere API affecting user experience
- Token length limitations with long conversation histories
- Database performance with growing conversation/message data

### How to Handle Conversation Persistence
- Strategy: Store conversation_id in localStorage with fallback to component state
- Consider: Session-based vs long-term persistence balance

### Spec Ambiguities
- get_user_info implementation: Need to determine exact source of user data from Better Auth
- Conversation title generation: How should conversation titles be created/updated?

## Recommended Next Action

Begin with Phase 1: Database Extensions to establish the foundational models. This is the most critical first step as all other components depend on the Conversation and Message models. After Phase 1 is complete, development can proceed in parallel tracks:
- Backend team can continue with Phases 2-5
- Frontend team can work on Phases 6-8

For testing, start with a curl command to the /api/chat endpoint after Phase 4 is complete, followed by full frontend integration testing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All constitutional principles upheld] |
