# Full-Stack TODO Web Application

This is a full-stack TODO application built with Next.js 16+, React 19, TypeScript, and FastAPI.

## Project Structure

```
├── backend/              # FastAPI backend
├── frontend/             # Next.js 16+ frontend
├── README.md             # This file
└── vercel.json           # Vercel deployment configuration
```

## Frontend (Next.js)

The frontend is located in the `frontend/` directory and includes:

- Modern UI with Tailwind CSS
- Authentication system
- Task management features
- Dashboard and calendar views
- Responsive design with dark/light mode

## Backend (FastAPI)

The backend is located in the `backend/` directory and includes:

- User authentication
- Task management API
- Database models with SQLModel
- JWT-based security

## Deployment

### Frontend Deployment

The frontend is designed to be deployed on Vercel:

1. Push your code to this GitHub repository
2. Go to [Vercel](https://vercel.com)
3. Create a new project and import this repository
4. Vercel will automatically detect the Next.js app in the `frontend/` directory
5. Set environment variables if needed:
   - `NEXT_PUBLIC_API_BASE_URL`: URL of your backend API
6. Deploy

### Backend Deployment

The backend can be deployed on platforms like:
- Railway
- Render
- Heroku
- Or any platform supporting Python/FastAPI applications

## Environment Variables

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend API

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request