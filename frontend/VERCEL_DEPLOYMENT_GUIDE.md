# Deploying Todo AI Chatbot Frontend to Vercel

This guide explains how to deploy the frontend of your Todo AI Chatbot application to Vercel.

## Prerequisites

- A GitHub account with the repository created
- A Vercel account (linked to your GitHub account)
- A deployed backend API (on Railway, Heroku, or similar platform)

## Step 1: Prepare Your Backend API

Before deploying the frontend, make sure your backend API is deployed and accessible:

1. Deploy your backend to a platform like Railway, Heroku, or Render
2. Note the deployed backend URL (e.g., `https://your-backend-production.up.railway.app`)
3. Make sure your backend is configured with proper CORS settings to allow requests from your frontend domain

## Step 2: Set Up Vercel Account

1. Go to [Vercel.com](https://vercel.com)
2. Sign up or log in to your account
3. Link your GitHub account when prompted

## Step 3: Import Your Repository

1. In your Vercel dashboard, click "Add New..." and select "Project"
2. Find and import your GitHub repository (`TODO-app-with-chatbot`)
3. If your repository has a monorepo structure (frontend and backend in the same repo), you'll need to configure the project to only build the frontend

## Step 4: Configure Monorepo (if applicable)

If your repository contains both frontend and backend in the same repository:

1. In the project configuration, set the "Root Directory" to `frontend`
2. Vercel should automatically detect that it's a Next.js project

## Step 5: Configure Build Settings

Vercel should automatically detect these settings, but verify them:

- **Framework Preset**: Next.js
- **Build Command**: `npm run build` (or `yarn build`)
- **Install Command**: `npm install` (or `yarn install`)
- **Output Directory**: `.next`

## Step 6: Set Environment Variables

Click on "Environment Variables" in your project settings and add:

- **Key**: `NEXT_PUBLIC_API_BASE_URL`
- **Value**: Your deployed backend API URL (e.g., `https://your-backend-production.up.railway.app/api`)

Make sure to add `/api` at the end if your backend serves API endpoints under that path.

## Step 7: Deploy

1. Click "Deploy" to start the deployment process
2. Vercel will install dependencies, build your application, and deploy it
3. Wait for the deployment to complete (usually takes 1-3 minutes)
4. Once complete, you'll see the deployment URL (e.g., `https://todo-app-with-chatbot.vercel.app`)

## Step 8: Configure Custom Domain (Optional)

If you want to use a custom domain:

1. In your Vercel project settings, go to "Domains"
2. Add your custom domain
3. Update your DNS settings as instructed by Vercel
4. Wait for DNS propagation (can take up to 48 hours)

## Step 9: Configure Backend CORS

Make sure your backend allows requests from your frontend domain:

1. In your backend, update CORS settings to include your Vercel deployment URL
2. If using the example above, add `https://todo-app-with-chatbot.vercel.app` to allowed origins
3. Redeploy your backend if necessary

## Step 10: Verify Deployment

1. Visit your deployed frontend URL
2. Register a new account
3. Test the chatbot functionality
4. Verify all task management features work correctly
5. Test conversation persistence

## Troubleshooting

### Common Issues:

1. **API Connection Errors**: Verify that `NEXT_PUBLIC_API_BASE_URL` is set correctly and your backend is accessible.

2. **CORS Errors**: Ensure your backend allows requests from your frontend domain.

3. **Build Failures**: Check that all dependencies are properly listed in `package.json`.

4. **Environment Variables Not Working**: Make sure variables are prefixed with `NEXT_PUBLIC_` to be available on the client-side.

### Useful Links:
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
- [Vercel Support](https://vercel.com/support)

## Continuous Deployment

Once configured, Vercel will automatically deploy new versions of your application whenever you push changes to your GitHub repository. You can configure this in your project settings under "Git" → "Deploy Hooks".

## Performance Optimization

Vercel automatically optimizes your Next.js application:
- Automatic image optimization
- Asset compression
- CDN distribution
- Server-side rendering optimization

## Monitoring

Monitor your application performance in the Vercel dashboard:
- View deployment logs
- Monitor performance metrics
- Track error rates
- Analyze visitor analytics

---

Your Todo AI Chatbot frontend is now ready to be deployed to Vercel! Follow these steps to get your application live on the internet.