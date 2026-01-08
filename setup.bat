@echo off
echo 🚀 Setting up LLM Data Copilot...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 20+
    exit /b 1
)

echo 📦 Setting up backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo 📦 Setting up frontend...
cd frontend
call yarn install
cd ..

echo 🗄️ Initializing database...
cd data
python init_db.py
cd ..

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Add your Groq API key to backend\.env
echo 2. Run start.bat to start both servers
pause
