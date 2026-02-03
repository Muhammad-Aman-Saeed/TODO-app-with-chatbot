#!/bin/sh
# vercel-build.sh - Script to help Vercel build the frontend

# Change to frontend directory and install dependencies
cd frontend
npm install --legacy-peer-deps
npm run build