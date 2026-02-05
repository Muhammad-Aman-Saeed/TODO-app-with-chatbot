# Todo AI Chatbot

An intelligent, state-aware Todo Assistant chatbot integrated inside a Todo web application with AI-powered natural language processing.

## Features

- **AI-Powered Task Management**: Use natural language to manage your tasks
- **Intelligent Assistant**: Ask the AI to add, list, complete, edit, or delete tasks
- **Secure Authentication**: JWT-based authentication with user isolation
- **Real-time Conversations**: Persistent conversation history
- **Responsive UI**: Beautiful, modern UI with dark/light mode support
- **Task Organization**: Add, edit, complete, and delete tasks with ease

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLModel with PostgreSQL
- **Authentication**: JWT tokens
- **AI Integration**: Cohere API for natural language processing
- **Deployment**: Designed for Railway, Heroku, or similar platforms

### Frontend
- **Framework**: Next.js 16+
- **Styling**: Tailwind CSS
- **UI Components**: Custom-built reusable components
- **Deployment**: Optimized for Vercel
- **State Management**: React hooks

## Architecture

```
├── backend/
│   ├── models.py           # Database models (User, Task, Conversation, Message)
│   ├── routes/
│   │   └── chat.py        # AI chat endpoint with Cohere integration
│   ├── services/
│   │   └── task_service.py # Business logic for task operations
│   ├── tools/
│   │   └── cohere_tools.py # Tool schemas and execution functions
│   └── utils/
│       └── mock_responses.py # Fallback responses when Cohere is unavailable
├── frontend/
│   ├── app/
│   │   └── dashboard/     # Main dashboard page
│   ├── components/
│   │   ├── ChatModal.tsx  # Chat interface component
│   │   ├── ChatbotIcon.tsx # Floating chatbot icon
│   │   └── TaskCard.tsx   # Task display component
│   ├── lib/
│   │   └── api.ts         # API client with JWT handling
│   └── types/
│       └── index.ts       # TypeScript type definitions
```

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- PostgreSQL (or use an online provider)
- Cohere API key (for AI features)

### Backend Setup

1. Navigate to the backend directory:
````
cd backend
```

2. Install dependencies:
````
pip install -r requirements.txt
```

3. Set up environment variables:
````
cp .env.example .env
```
Then edit `.env` with your configuration:
````
COHERE_API_KEY=your_cohere_api_key_here
BETTER_AUTH_SECRET=your_secure_jwt_secret_here
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
```

4. Run the backend:
````
python -m uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
````
cd frontend
```

2. Install dependencies:
````
npm install
```
or
````
yarn install
```

3. Set up environment variables:
````
cp .env.local.example .env.local
```
Then edit `.env.local` with your configuration:
````
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

4. Run the development server:
````
npm run dev
```
or
````
yarn dev
```

## AI Chatbot Capabilities

The chatbot understands natural language commands:

### Adding Tasks
- "Add a task to clean my room"
- "Create a task to buy groceries"
- "Remind me to call John tomorrow"

### Listing Tasks
- "Show me my tasks"
- "What tasks do I have?"
- "List my pending tasks"

### Completing Tasks
- "Complete task 1"
- "Mark 'buy groceries' as done"
- "I finished cleaning my room, mark it as complete"

### Deleting Tasks
- "Delete task 2"
- "Remove the meeting with Sarah"
- "Cancel 'call mom' task"

### Editing Tasks
- "Edit task 1 to say 'buy groceries and milk'"
- "Update the description of 'clean room' task"
- "Change the task 'buy food' to 'buy Groceries'"

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/auth/me` - Get current user

### Tasks
- `GET /api/tasks/` - Get all user tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

### Chat
- `POST /api/chat` - Chat with the AI assistant
- `GET /api/conversations/{id}/messages` - Get conversation history

## Environment Variables

### Backend
- `COHERE_API_KEY` - API key for Cohere AI service
- `BETTER_AUTH_SECRET` - Secret key for JWT tokens
- `DATABASE_URL` - Database connection string

### Frontend
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL

## Deployment

### Backend (Railway)
1. Create a new project on Railway
2. Connect to your GitHub repository
3. Set environment variables
4. Deploy the `backend` directory

### Frontend (Vercel)
1. Create a new project on Vercel
2. Connect to your GitHub repository
3. Set environment variables
4. Deploy the `frontend` directory

See the [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

## Security

- JWT-based authentication with proper token validation
- User isolation - users can only access their own data
- Input validation and sanitization
- Secure password hashing with bcrypt
- HTTPS enforcement in production

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue in the GitHub repository.

---

Built with ❤️ using FastAPI, Next.js, and AI technology."# TODO-app-with-chatbot" 
