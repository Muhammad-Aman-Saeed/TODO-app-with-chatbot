# Todo AI Chatbot - Frontend

This is the frontend for the Todo AI Chatbot application built with Next.js 16+ and TypeScript.

## Features

- **Modern UI**: Beautiful, responsive interface with dark/light mode
- **AI Chatbot**: Natural language interface for task management
- **Task Management**: Add, edit, complete, and delete tasks
- **Authentication**: Secure login and registration
- **Real-time Updates**: Live task management experience

## Tech Stack

- **Framework**: Next.js 16+ 
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **State Management**: React Hooks + TanStack Query

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
````
npm install
````
or
````
yarn install
```

2. Set up environment variables:
````
cp .env.local.example .env.local
````
Then edit `.env.local` with your configuration:
````
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

3. Run the development server:
````
npm run dev
````
or
````
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend API (e.g., `https://your-backend.onrender.com/api`)

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint

## Project Structure

```
├── app/                    # Next.js 16+ app directory
│   ├── dashboard/        # Main dashboard page
│   ├── auth/             # Authentication pages
│   └── layout.tsx        # Root layout
├── components/            # Reusable React components
│   ├── ui/               # UI components (buttons, modals, etc.)
│   ├── TaskCard.tsx      # Task display component
│   ├── ChatModal.tsx     # AI chat interface
│   └── ChatbotIcon.tsx   # Floating chatbot icon
├── lib/                   # Utility functions and API client
│   └── api.ts            # API client with JWT handling
├── types/                 # TypeScript type definitions
│   └── index.ts          # Shared types
├── hooks/                 # Custom React hooks
│   └── useAuth.ts        # Authentication hook
└── styles/                # Global styles
    └── globals.css       # Tailwind and custom styles
```

## Deployment

### Deploy on Vercel

The easiest way to deploy this Next.js application is to use [Vercel](https://vercel.com), the creators of Next.js.

You can deploy this application with a single command:

```bash
vercel
```

Or, you can import your Git repository into Vercel:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." and select "Project"
3. Import your Git repository
4. Configure the project:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Root Directory: `/` (or `frontend` if your repo has a monorepo structure)
5. Add environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend API URL
6. Click "Deploy"

### Environment Variables for Production

Make sure to set the following environment variable in your production environment:

- `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend API (e.g., `https://your-backend.onrender.com/api`)

## API Integration

The frontend communicates with the backend API through the centralized API client in `lib/api.ts`. All API calls include proper JWT authentication headers.

## Authentication

The application uses JWT-based authentication. The `useAuth` hook manages the authentication state and provides login/logout functionality.

## Styling

The application uses Tailwind CSS for styling with a custom design system. The global styles are in `styles/globals.css`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Support

If you encounter any issues, please file an issue in the GitHub repository.

---

Built with ❤️ using Next.js, TypeScript, and Tailwind CSS.