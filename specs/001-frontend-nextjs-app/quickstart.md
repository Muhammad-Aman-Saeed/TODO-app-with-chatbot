# Quickstart Guide: Frontend Next.js Application

## Overview
This guide provides the essential steps to set up, develop, and run the frontend Next.js application with Better Auth and premium UI design.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to backend API at http://localhost:8000/api

## Setup Instructions

### 1. Clone and Initialize
```bash
# Navigate to your project directory
cd hackathon-todo

# Create the frontend directory
mkdir frontend
cd frontend
```

### 2. Initialize Next.js Project
```bash
# Initialize a new Next.js project with TypeScript
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Or if you prefer to set it up manually:
npm init -y
npm install next react react-dom typescript @types/react @types/node @types/react-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 3. Install Required Dependencies
```bash
# Core dependencies
npm install better-auth @better-auth/jwt next-themes lucide-react framer-motion @tanstack/react-query

# Development dependencies
npm install -D @types/better-auth
```

### 4. Configure Tailwind CSS
Update `tailwind.config.ts` to include the premium design elements:

```ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {
      colors: {
        // Soft color palette as specified
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        secondary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
      },
      boxShadow: {
        // Subtle shadows for premium feel
        'soft': '0 2px 4px rgba(0, 0, 0, 0.04), 0 4px 8px rgba(0, 0, 0, 0.04)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.15)',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },
      backdropBlur: {
        'xs': '2px',
      }
    },
  },
  plugins: [],
}
export default config
```

### 5. Configure Next.js
Update `next.config.js`:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    typedRoutes: true,
  },
  images: {
    domains: ['lh3.googleusercontent.com', 'avatars.githubusercontent.com'], // For social login avatars
  },
}

module.exports = nextConfig
```

### 6. Set Up Better Auth
Create `src/lib/auth.ts`:

```ts
import { betterAuth } from "better-auth";
import { jwt } from "@better-auth/jwt";

export const auth = betterAuth({
  secret: process.env.AUTH_SECRET || "fallback-secret-for-development",
  database: {
    provider: "sqlite",
    url: process.env.DATABASE_URL || "./db.sqlite",
  },
  plugins: [
    jwt({
      secret: process.env.JWT_SECRET || "fallback-jwt-secret",
    }),
  ],
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    },
  },
});
```

### 7. Create API Client
Create `src/lib/api.ts`:

```ts
import { auth } from '@/lib/auth';

// Base API client that automatically attaches JWT
class ApiClient {
  private baseUrl: string;
  
  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';
  }

  // Helper to get JWT token
  private async getJwtToken(): Promise<string | null> {
    // Implementation to retrieve JWT from storage or session
    if (typeof window !== 'undefined') {
      // Client-side: get from localStorage or session
      return localStorage.getItem('jwt_token');
    }
    // Server-side: would need to implement differently
    return null;
  }

  // Generic request method that adds JWT header
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getJwtToken();
    
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
  }

  // Specific API methods
  async getTasks(): Promise<any[]> {
    return this.request('/tasks');
  }

  async createTask(taskData: any): Promise<any> {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id: string, taskData: any): Promise<any> {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id: string): Promise<void> {
    await this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleComplete(id: string, completed: boolean): Promise<any> {
    return this.request(`/tasks/${id}/toggle`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }
}

export const apiClient = new ApiClient();
```

## Development Workflow

### Running the Development Server
```bash
npm run dev
# or
yarn dev
```

Visit `http://localhost:3000` to see your application.

### Building for Production
```bash
npm run build
npm start
```

## Key Files and Directories

### App Router Structure
```
src/app/
├── layout.tsx          # Root layout with providers
├── page.tsx            # Home page (redirects to dashboard/auth)
├── auth/
│   ├── sign-in/
│   │   └── page.tsx    # Sign-in page
│   └── sign-up/
│       └── page.tsx    # Sign-up page
└── dashboard/
    └── page.tsx        # Main dashboard
```

### Component Structure
```
src/components/
├── ui/                 # Base UI components (Button, Input, etc.)
├── TaskCard.tsx        # Beautiful task card component
├── TaskForm.tsx        # Form for creating/editing tasks
├── Modal.tsx           # Reusable modal component
├── Navbar.tsx          # Navigation component
└── Sidebar.tsx         # Sidebar navigation
```

### Utility Structure
```
src/lib/
├── api.ts              # Centralized API client with JWT handling
├── auth.ts             # Better Auth configuration
└── utils.ts            # General utility functions
```

## Environment Variables
Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
AUTH_SECRET=your-auth-secret-here
JWT_SECRET=your-jwt-secret-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Premium UI Guidelines

### Color Palette
- Primary colors: Indigo shades (#0ea5e9, #0284c7, #0369a1)
- Secondary colors: Emerald shades (#14b8a6, #0d9488, #0f766e)
- Neutral colors: Slate shades (#64748b, #475569, #334155)

### Design Elements
- Rounded corners: Use `rounded-xl`, `rounded-2xl`, `rounded-3xl` for soft edges
- Subtle shadows: Apply `shadow-soft` for premium feel
- Smooth transitions: Use `transition-all duration-300` for interactions
- Glassmorphism: Use `bg-white/80 dark:bg-slate-800/80 backdrop-blur-xs` with `shadow-glass`

### Responsive Design
- Mobile-first approach with Tailwind's responsive prefixes
- Use `sm:`, `md:`, `lg:`, `xl:` prefixes appropriately
- Implement touch-friendly controls for mobile devices

## Next Steps
1. Implement the authentication flow with Better Auth
2. Create the premium UI components following the design guidelines
3. Connect the dashboard to the API using the centralized client
4. Add dark mode support using next-themes
5. Implement task CRUD operations with proper loading and error states