# Hackathon Todo App - Frontend

A professional, modern Next.js 16+ frontend application with TypeScript, Tailwind CSS, and premium UI design. Features include authentication, task management, and responsive design with dark mode support.

## Features

- 🎨 **Premium UI Design**: Soft color palette (slate, indigo, emerald), subtle shadows, glassmorphism effects
- 🔐 **Authentication**: Secure user registration and login with JWT tokens
- 📋 **Task Management**: Create, read, update, and delete tasks with filtering
- 🌙 **Dark Mode**: Toggle between light and dark themes with system preference detection
- 📱 **Responsive**: Fully responsive design for mobile, tablet, and desktop
- ⚡ **Performance**: Optimized with animations and smooth transitions
- 🧭 **Navigation**: Intuitive sidebar navigation for enhanced UX

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+ with custom premium design
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **State Management**: React Hooks
- **API Client**: Custom implementation with automatic JWT handling

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the root directory with the following:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Home page
│   │   ├── auth/          # Authentication pages
│   │   │   ├── sign-in/   # Sign-in page
│   │   │   └── sign-up/   # Sign-up page
│   │   └── dashboard/     # Dashboard page
│   ├── components/        # Reusable UI components
│   │   ├── ui/            # Base UI components
│   │   ├── TaskCard.tsx   # Beautiful task card component
│   │   ├── TaskForm.tsx   # Form for creating/editing tasks
│   │   ├── Modal.tsx      # Reusable modal component
│   │   ├── Navbar.tsx     # Navigation component
│   │   └── Sidebar.tsx    # Sidebar navigation
│   ├── lib/               # Utilities and API client
│   │   ├── api.ts         # Centralized API client with JWT handling
│   │   └── utils.ts       # General utility functions
│   ├── hooks/             # Custom React hooks
│   │   └── useAuth.ts     # Authentication hook
│   ├── styles/            # Global styles
│   │   └── globals.css    # Tailwind imports and global styles
│   └── types/             # TypeScript type definitions
│       └── index.ts       # Common type definitions
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The base URL for the backend API (default: http://localhost:8000/api)

## Scripts

- `npm run dev`: Start the development server
- `npm run build`: Build the application for production
- `npm run start`: Start the production server
- `npm run lint`: Run ESLint

## API Integration

The frontend communicates with the backend API at the configured base URL. The API client in `src/lib/api.ts` handles authentication by automatically attaching JWT tokens to requests.

## Design System

### Color Palette
- Primary: Indigo shades (#0ea5e9, #0284c7, #0369a1)
- Secondary: Emerald shades (#14b8a6, #0d9488, #0f766e)
- Neutral: Slate shades (#64748b, #475569, #334155)

### Design Elements
- Rounded corners: Use `rounded-xl`, `rounded-2xl`, `rounded-3xl` for soft edges
- Subtle shadows: Apply `shadow-soft` for premium feel
- Smooth transitions: Use `transition-all duration-300` for interactions
- Glassmorphism: Use `bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm` with `shadow-glass`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.