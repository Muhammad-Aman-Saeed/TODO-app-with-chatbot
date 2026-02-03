#!/bin/bash
# vercel-build.sh - Build script for Vercel deployment

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
  echo "Error: frontend directory does not exist"
  ls -la  # List all files to debug
  exit 1
fi

# Change to frontend directory and run build
cd frontend
npm install --legacy-peer-deps
npm run build