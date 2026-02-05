# Deploying Todo AI Chatbot Frontend to Vercel (Connected to Hugging Face Backend)

This guide explains how to deploy the frontend of your Todo AI Chatbot application to Vercel, connected to your backend deployed on Hugging Face Spaces.

## Prerequisites

- A GitHub account with the repository created (https://github.com/Muhammad-Aman-Saeed/TODO-app-with-chatbot)
- A Vercel account (linked to your GitHub account)
- Your backend deployed on Hugging Face Spaces (https://amansaeed-todo-app-with-chatbot.hf.space)

## Step 1: Verify Your Backend URL

Your backend is deployed at: `https://amansaeed-todo-app-with-chatbot.hf.space`

Note: Hugging Face Spaces typically serve APIs at the root URL, but check if your backend API endpoints are served at:
- `https://amansaeed-todo-app-with-chatbot.hf.space` (root)
- OR `https://amansaeed-todo-app-with-chatbot.hf.space/api` (with /api suffix)

## Step 2: Set Up Vercel Account

1. Go to [Vercel.com](https://vercel.com)
2. Sign up or log in to your account
3. Link your GitHub account when prompted

## Step 3: Import Your Repository

1. In your Vercel dashboard, click "Add New..." and select "Project"
2. Find and import your GitHub repository (`TODO-app-with-chatbot`)
3. Since your repository has both frontend and backend (monorepo structure), you need to configure the project to only build the frontend

## Step 4: Configure Monorepo Build Settings

1. In the project configuration, set the "Root Directory" to `frontend`
2. Vercel should automatically detect that it's a Next.js project

## Step 5: Configure Build Settings

Vercel should automatically detect these settings, but verify them:

- **Framework Preset**: Next.js
- **Build Command**: `npm run build` (or `yarn build`)
- **Install Command**: `npm install` (or `yarn install`)
- **Output Directory**: `.next`
- **Root Directory**: `frontend` (important for monorepo)

## Step 6: Set Environment Variables

Click on "Environment Variables" in your project settings and add:

- **Key**: `NEXT_PUBLIC_API_BASE_URL`
- **Value**: `https://amansaeed-todo-app-with-chatbot.hf.space` (or `https://amansaeed-todo-app-with-chatbot.hf.space/api` if your API endpoints are under /api)

## Step 7: Deploy

1. Click "Deploy" to start the deployment process
2. Vercel will install dependencies, build your application, and deploy it
3. Wait for the deployment to complete (usually takes 1-3 minutes)
4. Once complete, you'll see the deployment URL (e.g., `https://todo-app-with-chatbot.vercel.app`)

## Step 8: Configure CORS on Your Hugging Face Space

Since your backend is on Hugging Face Spaces and frontend will be on Vercel, you need to ensure CORS is properly configured:

1. In your Hugging Face Space, make sure CORS is enabled for your domain
2. If you have control over the backend code in your Space, ensure it allows requests from your Vercel domain
3. The Hugging Face Space should allow requests from your Vercel deployment URL

## Step 9: Verify Deployment

1. Visit your deployed frontend URL from Vercel
2. Register a new account
3. Test the chatbot functionality
4. Verify all task management features work correctly
5. Test conversation persistence

## Troubleshooting

### Common Issues:

1. **CORS Errors**: If you get CORS errors, this means your Hugging Face Space backend isn't configured to allow requests from your Vercel frontend domain. You may need to update CORS settings in your backend.

2. **API Connection Errors**: Verify that `NEXT_PUBLIC_API_BASE_URL` is set correctly to your Hugging Face Space URL.

3. **Build Failures**: Make sure you've set the "Root Directory" to `frontend` in your Vercel project settings.

4. **Authentication Issues**: Ensure JWT tokens can be properly stored and sent between domains.

### Testing Your Backend API

You can test if your backend API is accessible by visiting:
- `https://amansaeed-todo-app-with-chatbot.hf.space/health` (health check)
- `https://amansaeed-todo-app-with-chatbot.hf.space/docs` (API documentation)

## Important Notes

- Hugging Face Spaces may have some limitations compared to dedicated hosting platforms
- If you experience CORS issues, you might need to add CORS middleware to your backend
- Your backend on Hugging Face may go to sleep when inactive, causing slower initial responses

## Updating CORS in Your Backend (if needed)

If you encounter CORS issues, you'll need to update your backend's CORS configuration in `backend/main.py`:

```python
# Add your Vercel domain to allowed origins
allowed_origins = [
    "http://localhost:3000",  # For local development
    "https://your-vercel-domain.vercel.app",  # Replace with your actual Vercel domain
    # Add other domains as needed
]
```

## Next Steps

1. Deploy your frontend to Vercel using the above instructions
2. Test the connection between frontend and backend
3. If you encounter CORS issues, update your backend configuration
4. Share your fully deployed application!

---

Your Todo AI Chatbot frontend is now ready to be deployed to Vercel and connected to your Hugging Face backend! Follow these steps to get your complete application live.