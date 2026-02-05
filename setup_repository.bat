@echo off
REM Setup script for Todo AI Chatbot project

echo Welcome to the Todo AI Chatbot Setup!
echo ======================================

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git and add it to your PATH before continuing.
    pause
    exit /b 1
)

REM Check if node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Node.js is not installed or not in PATH.
    echo This is required for the frontend.
) else (
    echo Node.js: OK
)

REM Check if python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python is not installed or not in PATH.
    echo This is required for the backend.
) else (
    echo Python: OK
)

echo.
echo To create a new GitHub repository and deploy this project:
echo 1. Go to GitHub.com and create a new repository
echo 2. Copy the repository URL
echo 3. Clone the repository to a new location
echo 4. Copy all files from this project to the new repository
echo 5. Follow the deployment guide in DEPLOYMENT_GUIDE.md

echo.
echo Current project structure:
dir /AD /ON

echo.
echo Files ready for transfer to new repository:
echo - All backend files in /backend/
echo - All frontend files in /frontend/
echo - README.md
echo - DEPLOYMENT_GUIDE.md
echo - LICENSE
echo - .gitignore

echo.
echo For detailed deployment instructions, see DEPLOYMENT_GUIDE.md
pause