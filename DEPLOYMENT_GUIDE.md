# Todo AI Chatbot - Deployment Guide

This guide explains how to create a new GitHub repository and deploy the Todo AI Chatbot project.

## Prerequisites

- GitHub account
- Git installed locally
- Node.js and npm/yarn for frontend
- Python 3.8+ for backend
- Access to deployment platforms (Vercel for frontend, Railway/Heroku for backend)

## Step 1: Create New GitHub Repository

1. Go to GitHub.com and log in to your account
2. Click the "+" icon in the top right corner and select "New repository"
3. Enter repository name (e.g., "todo-ai-chatbot")
4. Add a description
5. Choose "Public" or "Private" as per your preference
6. Check "Add a README file"
7. Select "MIT License" (or your preferred license)
8. Click "Create repository"

## Step 2: Clone and Prepare the Project

```bash
# Clone the new repository
git clone https://github.com/YOUR_USERNAME/todo-ai-chatbot.git
cd todo-ai-chatbot

# Copy your project files to this directory
# (Copy all files from your current project to this directory)

# Initialize git and add all files
git add .
git commit -m "Initial commit: Todo AI Chatbot project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/todo-ai-chatbot.git
git push -u origin main
```

## Step 3: Backend Deployment (Railway)

### 1. Set Up Railway Account
- Go to [Railway.app](https://railway.app)
- Sign in with your GitHub account

### 2. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your "todo-ai-chatbot" repository
- Select the "backend" directory

### 3. Configure Environment Variables
Add the following environment variables in Railway:
```
COHERE_API_KEY=your_cohere_api_key_here
BETTER_AUTH_SECRET=your_secure_jwt_secret_here
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### 4. Configure Build Settings
In Railway's settings, set the build command to:
````
cd backend && pip install -r requirements.txt
```

And the start command to:
````
cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Step 4: Frontend Deployment (Vercel)

### 1. Set Up Vercel Account
- Go to [Vercel.com](https://vercel.com)
- Sign in with your GitHub account

### 2. Create New Project
- Click "New Project"
- Import your "todo-ai-chatbot" repository
- Select the "frontend" directory

### 3. Configure Environment Variables
Add the following environment variables in Vercel:
```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.railway.app
```

### 4. Configure Build Settings
- Framework Preset: Next.js
- Build Command: `cd frontend && npm run build`
- Root Directory: `frontend`

## Step 5: Database Setup

### Option 1: Railway Database
- In your Railway project, click "New" → "Database"
- Select "PostgreSQL" or "MySQL"
- Railway will automatically add the DATABASE_URL environment variable

### Option 2: External Database
- Use a database provider like Neon, Supabase, or AWS RDS
- Update the DATABASE_URL environment variable accordingly

## Step 6: Authentication Setup

### Better Auth Configuration
- Follow Better Auth documentation to set up authentication
- Configure OAuth providers if needed
- Ensure JWT secrets are properly configured

## Step 7: AI Service Configuration

### Cohere API Setup
- Sign up at [Cohere](https://cohere.ai)
- Create an API key
- Add the API key to your backend environment variables

## Step 8: Update Frontend Configuration

Update the `NEXT_PUBLIC_API_BASE_URL` in your frontend environment to point to your deployed backend URL.

## Step 9: Verification

1. Visit your deployed frontend URL
2. Register a new account
3. Test the chatbot functionality
4. Verify all task management features work correctly
5. Test conversation persistence

## Additional Configuration

### Custom Domain (Optional)
- Purchase a domain name
- Configure DNS settings to point to your Vercel and Railway deployments
- Set up SSL certificates

### Monitoring and Analytics
- Set up error monitoring (Sentry, LogRocket)
- Add analytics (Google Analytics, Plausible)

## Troubleshooting

### Common Issues:

1. **Environment Variables Not Set**: Ensure all required environment variables are set in both frontend and backend deployments.

2. **CORS Issues**: Make sure your backend allows requests from your frontend domain.

3. **Database Connection**: Verify your database URL is correctly configured and accessible.

4. **Authentication Issues**: Check that JWT secrets match between frontend and backend.

## Maintenance

- Regularly update dependencies
- Monitor application logs
- Backup database regularly
- Rotate API keys periodically

---

Your Todo AI Chatbot project is now ready for deployment! Follow these steps to get your application live on the internet.