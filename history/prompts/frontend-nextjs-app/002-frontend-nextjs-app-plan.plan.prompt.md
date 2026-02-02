---
id: "002"
title: "frontend-nextjs-app-plan"
stage: "plan"
date_iso: "2026-02-01"
surface: "agent"
model: "Claude Sonnet 4"
feature: "frontend-nextjs-app"
branch: "001-frontend-nextjs-app"
user: "user"
command: "/sp.plan You are the Project Planning Agent for the hackathon-todo Phase 2 frontend.

Your task: Create a detailed, step-by-step implementation plan for the entire /frontend folder based on the following specification.

SPECIFICATION SUMMARY (strictly follow this):
- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS with modern 2025 premium design: soft palette (slate/indigo/emerald), subtle shadows, glassmorphism/neumorphism, smooth transitions, dark mode, fully responsive
- Beautiful, professional UI: premium task cards, gradient login pages, modern dashboard with filters and modal
- Better Auth with JWT plugin enabled
- After login → fetch JWT from /api/auth/token
- Centralized API client (/lib/api.ts) that automatically attaches Authorization: Bearer <token>
- Key pages: root redirect, sign-in, sign-up, dashboard (protected)
- Reusable styled components (TaskCard, TaskForm, Modal, etc.)
- Icons: lucide-react or heroicons
- Optional: framer-motion for subtle animations
- Server Components default, Client Components only where needed

OUTPUT A COMPREHENSIVE PLAN IN THIS EXACT STRUCTURE:

1. **Overall Goals & Success Criteria**
   - What makes this frontend "complete" for Phase 2?
   - Key visual and functional benchmarks

2. **Folder Structure Plan**
   - Complete /frontend directory tree with all files and folders
   - Justification for organization

3. **Dependencies & Setup (Phase 1)**
   - List all required npm packages with exact names (better-auth, plugins, icons, etc.)
   - Configuration files needed (package.json scripts, tailwind.config.ts, etc.)

4. **Phased Implementation Steps** (Break into 5-7 logical phases)
   Each phase must include:
   - Phase name
   - Goal
   - Files to create/modify
   - Dependencies on previous phases
   - Estimated complexity
   - Visual/UI focus (e.g., "Premium login page with gradient background")

   Suggested phases (you can refine):
   - Phase 1: Base Next.js + Tailwind setup
   - Phase 2: Better Auth integration + JWT token fetching
   - Phase 3: API client with auto JWT attachment
   - Phase 4: Authentication pages (sign-in/sign-up) with premium design
   - Phase 5: Protected dashboard layout + navigation
   - Phase 6: Task list UI with filters and beautiful TaskCard component
   - Phase 7: Add/Edit task modal + form with smooth UX
   - Phase 8: Polish – dark mode, animations, responsiveness

5. **UI/Design System Plan**
   - Color palette (exact Tailwind classes)
   - Typography scale
   - Component design guidelines (Card, Button, Input, Modal)
   - Icon strategy
   - Animation approach

6. **Risks & Open Questions**
   - Any ambiguity in Better Auth JWT flow?
   - How to handle token refresh?
   - Protected route strategy in App Router?

7. **Next Action Recommendation**
   - Which phase or file to implement first after this plan is approved?

Do not write any code in this response.
Output only the structured plan above.
Be extremely detailed and professional — this plan will guide the entire frontend development."
labels: ["planning", "frontend", "nextjs", "architecture"]
links:
  spec: "./spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-frontend-nextjs-app/plan.md"
  - "specs/001-frontend-nextjs-app/research.md"
  - "specs/001-frontend-nextjs-app/data-model.md"
  - "specs/001-frontend-nextjs-app/quickstart.md"
  - "specs/001-frontend-nextjs-app/contracts/api-contracts.md"
tests_yaml: []
---

# Implementation Plan: Frontend Next.js Application

## Summary

Comprehensive implementation plan for a professional, modern Next.js 16+ frontend application with TypeScript, Tailwind CSS, and Better Auth integration. The application features a premium UI with soft color palette, responsive design, dark mode support, and JWT-based authentication.

## Details

**Branch**: `001-frontend-nextjs-app`
**Date**: 2026-02-01
**Spec**: [link to spec.md](./spec.md)

### Overall Goals & Success Criteria

The frontend is "complete" when it:
- Allows users to register and authenticate securely using Better Auth
- Provides a responsive dashboard for managing tasks (CRUD operations)
- Implements premium UI design with soft color palette, subtle shadows, glassmorphism effects
- Supports dark/light mode with user preference persistence
- Works seamlessly across mobile, tablet, and desktop devices
- Includes proper error handling and loading states

### Folder Structure Plan

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── app/                    # Next.js 16+ App Router
│   │   ├── layout.tsx          # Root layout with providers
│   │   ├── page.tsx            # Home page (redirects to dashboard/auth)
│   │   ├── auth/
│   │   │   ├── sign-in/
│   │   │   │   └── page.tsx    # Sign-in page
│   │   │   └── sign-up/
│   │   │       └── page.tsx    # Sign-up page
│   │   └── dashboard/
│   │       └── page.tsx        # Main dashboard
│   ├── components/             # Reusable UI components
│   │   ├── ui/                 # Base UI components (Button, Input, etc.)
│   │   ├── TaskCard.tsx        # Beautiful task card component
│   │   ├── TaskForm.tsx        # Form for creating/editing tasks
│   │   ├── Modal.tsx           # Reusable modal component
│   │   ├── Navbar.tsx          # Navigation component
│   │   └── Sidebar.tsx         # Sidebar navigation
│   ├── lib/                    # Utility functions
│   │   ├── api.ts              # Centralized API client with JWT handling
│   │   └── utils.ts            # General utility functions
│   ├── hooks/                  # Custom React hooks
│   │   └── useAuth.ts          # Authentication hook
│   ├── styles/                 # Global styles
│   │   └── globals.css         # Tailwind imports and global styles
│   └── types/                  # TypeScript type definitions
│       └── index.ts            # Common type definitions
├── package.json               # Dependencies and scripts
├── tsconfig.json              # TypeScript configuration
├── next.config.js             # Next.js configuration
├── tailwind.config.ts         # Tailwind CSS configuration
└── README.md                  # Project documentation
```

### Dependencies & Setup

- Next.js 16+
- React 19+
- TypeScript 5.x
- Tailwind CSS 3+
- Better Auth
- @better-auth/jwt
- Lucide React
- Framer Motion (optional)
- @tanstack/react-query

Configuration files:
- package.json
- tsconfig.json
- next.config.js
- tailwind.config.ts
- .env.local

### Phased Implementation Steps

1. **Phase 1: Base Next.js + Tailwind Setup**
   - Goal: Establish project foundation with proper configuration
   - Files: package.json, tsconfig.json, next.config.js, tailwind.config.ts, globals.css
   - Dependencies: None
   - Complexity: Low
   - UI Focus: Basic styling setup

2. **Phase 2: Better Auth Integration + JWT Token Fetching**
   - Goal: Implement authentication system with JWT handling
   - Files: lib/auth.ts, auth pages, session management
   - Dependencies: Phase 1
   - Complexity: Medium
   - UI Focus: Authentication infrastructure

3. **Phase 3: API Client with Auto JWT Attachment**
   - Goal: Create centralized API client that handles authentication
   - Files: lib/api.ts
   - Dependencies: Phase 2
   - Complexity: Medium
   - UI Focus: Backend connectivity

4. **Phase 4: Authentication Pages with Premium Design**
   - Goal: Create beautiful sign-in/sign-up pages
   - Files: app/auth/sign-in/page.tsx, app/auth/sign-up/page.tsx
   - Dependencies: Phase 1-3
   - Complexity: Medium
   - UI Focus: Premium login page with gradient background

5. **Phase 5: Protected Dashboard Layout + Navigation**
   - Goal: Implement protected dashboard with navigation
   - Files: app/dashboard/page.tsx, components/Navbar.tsx, components/Sidebar.tsx
   - Dependencies: Phase 1-4
   - Complexity: High
   - UI Focus: Dashboard layout with premium design

6. **Phase 6: Task List UI with Filters and TaskCard Component**
   - Goal: Display tasks with filtering capabilities
   - Files: components/TaskCard.tsx, dashboard page logic
   - Dependencies: Phase 1-5
   - Complexity: High
   - UI Focus: Beautiful task cards with status indicators

7. **Phase 7: Add/Edit Task Modal with Smooth UX**
   - Goal: Implement task creation and editing functionality
   - Files: components/TaskForm.tsx, components/Modal.tsx
   - Dependencies: Phase 1-6
   - Complexity: Medium
   - UI Focus: Smooth modal interactions

8. **Phase 8: Polish – Dark Mode, Animations, Responsiveness**
   - Goal: Enhance UI with premium touches
   - Files: Various components, globals.css, theme handling
   - Dependencies: All previous phases
   - Complexity: Medium
   - UI Focus: Dark mode, animations, responsive design

### UI/Design System Plan

- **Color Palette**: Soft slate, indigo, and emerald shades using Tailwind classes
- **Typography**: Modern font stack with appropriate sizing hierarchy
- **Component Design**: Consistent rounded corners, subtle shadows, smooth transitions
- **Icon Strategy**: Lucide React for consistent iconography
- **Animation Approach**: Framer Motion for subtle entrance animations and transitions

### Risks & Open Questions

- JWT token refresh mechanism needs implementation
- Protected route handling in App Router requires careful implementation
- Cross-browser compatibility for advanced CSS features
- Performance considerations with large task lists

### Next Action Recommendation

Begin with Phase 1: Base Next.js + Tailwind setup to establish the project foundation.

## Outcome

The implementation plan is complete with detailed phases, dependencies, and UI focus areas. All necessary supporting documents have been created including research, data models, quickstart guide, and API contracts. The agent context has been updated with the relevant technologies for this feature.