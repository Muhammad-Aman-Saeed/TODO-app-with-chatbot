---
id: 3
title: Create AI Chatbot Implementation Plan
stage: plan
date_iso: 2026-02-04
surface: agent
model: Qwen
feature: ai-chatbot-integration
branch: 003-ai-chatbot-integration
user: user
command: /sp.plan
labels:
  - planning
  - ai
  - chatbot
  - architecture
links:
  spec: specs/003-ai-chatbot-integration/spec.md
  plan: specs/003-ai-chatbot-integration/plan.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/003-ai-chatbot-integration/plan.md
  - specs/003-ai-chatbot-integration/research.md
  - specs/003-ai-chatbot-integration/data-model.md
  - specs/003-ai-chatbot-integration/contracts/chat-api-contract.md
  - specs/003-ai-chatbot-integration/quickstart.md
tests_yaml: []
---

# Create AI Chatbot Implementation Plan

## User Input

```
/sp.plan You are the Project Planning Agent for Phase III: AI Todo Chatbot with Cohere integration in the hackathon-todo monorepo.

Your task: Create a comprehensive, step-by-step implementation plan based exactly on the provided sp.specify specification.

SPECIFICATION SUMMARY (do NOT deviate or add features outside this):
- Integrate inside existing Phase II backend (FastAPI + SQLModel + Better Auth JWT)
- Use Cohere API (COHERE_API_KEY from .env) as LLM with native tool calling
- Preferred model: command-r-plus (fallback command-a)
- Exactly 5 tools: add_task, list_tasks, complete_task, delete_task, get_user_info
- All tools validate user_id == authenticated user_id
- New models: Conversation & Message (add to existing models.py)
- New endpoint: POST /api/chat (JWT protected, stateless via DB)
- Chat flow: load history → Cohere chat() with tools → execute tools if called → save messages → return response
- System prompt: friendly Todo assistant with tool usage rules
- Frontend: Add floating chatbot icon (bottom-right) in dashboard → open modal/slide-in chat panel
- Chat UI: message bubbles, input, loading, auto-scroll, conversation continuity via localStorage/state
- API client update: add chat() function in /lib/api.ts with JWT header

OUTPUT MUST FOLLOW THIS EXACT STRUCTURE (detailed aur professional rakho):

1. **Overall Goals & Success Criteria**
   - What makes Phase III "successfully complete"?
   - Key integration checkpoints (backend ↔ frontend, Cohere ↔ tools, DB persistence)
   - Security & UX benchmarks (user isolation, smooth chat, beautiful UI)

2. **Folder Structure Changes Plan**
   - Only show NEW / UPDATED files & folders
   - Full paths with brief purpose
   - Example:
     backend/
     ├── models.py                  # append Conversation & Message
     ├── routes/chat.py             # new file for /api/chat
     ├── services/task_service.py   # tool execution logic (recommended)
     ├── tools/cohere_tools.py      # tool JSON schemas + executor functions
     frontend/
     ├── components/ChatbotIcon.tsx
     ├── components/ChatModal.tsx   # or ChatPanel.tsx
     └── lib/api.ts                 # updated with chat method

3. **Dependencies & Environment Setup**
   - New pip packages (backend)
   - New npm packages (frontend, if any – e.g., lucide-react already hai to mention)
   - .env additions (COHERE_API_KEY)
   - Any migration note (manual or alembic if using)

4. **Phased Implementation Steps** (7–9 logical phases – sequential aur dependency-aware)
   Har phase mein ye include karo:
   - Phase number & name
   - Goal / objective
   - Files to create / modify
   - Key technical decisions (e.g., tool schema format, history limit, modal vs drawer)
   - Dependencies on previous phases
   - Security / integration focus
   - Complexity level (low / medium / high)
   - Visual / UX notes for frontend phases

   Suggested phases (tum improve kar sakte ho):
   - Phase 1: Database extensions (add Conversation & Message models)
   - Phase 2: Define Cohere tool schemas & execution functions
   - Phase 3: Build tool service layer (validate user_id + reuse Phase II CRUD)
   - Phase 4: Implement POST /api/chat endpoint with Cohere chat logic
   - Phase 5: Handle tool calls loop (multi-turn if Cohere returns multiple)
   - Phase 6: Frontend – add floating chatbot icon & trigger logic in dashboard
   - Phase 7: Build chat modal/panel UI (bubbles, input, loading, history fetch)
   - Phase 8: Update api.ts client → add chat() method + error handling
   - Phase 9: Polish & testing plan (conversation resume, dark mode, animations)

5. **UI/UX & Design System Plan (Frontend)**
   - Floating icon style (position, color, hover effect)
   - Chat modal design (size, position, Tailwind classes, dark mode)
   - Message bubble styles (user vs assistant)
   - Animation suggestions (framer-motion optional)
   - Accessibility notes (focus management, aria labels)

6. **Risks, Assumptions & Clarifications Needed**
   - Assumption on Cohere tool call format & response structure
   - Potential issues: rate limits, token length for long histories
   - How to handle conversation_id persistence (localStorage vs session)
   - Any spec ambiguity (e.g., get_user_info implementation)

7. **Recommended Next Action**
   - Which phase should be implemented first after this plan is approved?
   - Suggested test flow after completion (e.g., curl /api/chat, then frontend chat)

Do NOT write any code in this response.
Output ONLY the structured plan above — detailed, clear, and ready to guide implementation.
```

## Response Summary

Created a comprehensive implementation plan for the AI Todo Chatbot Integration feature. The plan includes:

1. Detailed technical context and constitution check
2. Overall goals and success criteria
3. Complete folder structure changes plan
4. Dependencies and environment setup requirements
5. Nine phased implementation steps with detailed goals, files, and complexity ratings
6. UI/UX and design system plan for frontend components
7. Risk assessment and assumptions
8. Recommended next actions

Additionally, created supporting documents:
- Research.md: Captures key decisions and rationale
- Data-model.md: Defines Conversation and Message entities
- API contract: Specifies the /api/chat endpoint
- Quickstart guide: Provides implementation walkthrough

## Outcome

Successfully created a complete implementation plan that aligns with the feature specification and project constitution. The plan is structured in phases with clear dependencies and security considerations, ready to guide the development team through implementation.