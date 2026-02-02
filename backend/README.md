---
title: Hackathon Todo Backend API
emoji: 🚀
colorFrom: purple
colorTo: yellow
sdk: docker
runtime: cpython
app_file: run_server.py
pinned: false
license: mit
---

# Hackathon Todo Backend API

Secure task management API with JWT authentication built with FastAPI.

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login existing user
- `GET /api/auth/token` - Validate JWT token
- `GET /api/tasks/` - Get all tasks for authenticated user
- `POST /api/tasks/` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Environment Variables

- `SECRET_KEY` - Secret key for JWT encoding/decoding
- `DATABASE_URL` - Database connection string (defaults to SQLite)