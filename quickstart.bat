@echo off
REM Quick Start Script - AI Hiring Assistant (Windows)
REM Supports: Local and Docker deployments

setlocal enabledelayedexpansion

REM Colors (Windows 10+ with ANSI support)
set BLUE=[0;34m
set GREEN=[0;32m
set YELLOW=[1;33m
set RED=[0;31m
set NC=[0m

cls

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     🤖 AI Hiring Assistant - Quick Start               ║
echo ║     CrewAI Multi-Agent System v0.1                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo [INFO] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check/create .env
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo [OK] Created .env from template
        echo [WARNING] Please update OPENAI_API_KEY in .env
        pause
    )
) else (
    echo [OK] .env already exists
)

echo.
echo Choose deployment method:
echo 1) Local (Python + venv)
echo 2) Docker (Recommended)
echo 3) Test API
echo 4) Exit
echo.

set /p choice="Enter choice [1-4]: "

if "%choice%"=="1" goto local_deploy
if "%choice%"=="2" goto docker_deploy
if "%choice%"=="3" goto test_api
if "%choice%"=="4" goto exit_script
goto menu

:local_deploy
echo.
echo [INFO] Deploying locally...

REM Create venv if not exists
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -q -r requirements.txt
echo [OK] Dependencies installed
echo.
echo [OK] Ready to start!
echo.
echo Start the API server:
echo   python -m src.api.main
echo.
echo In another terminal, start Streamlit UI:
echo   streamlit run src/ui/streamlit_app.py
echo.
echo Access URLs:
echo   API: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo   UI: http://localhost:8501
echo.
pause
goto end

:docker_deploy
echo.
echo [INFO] Deploying with Docker...

docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed!
    echo [INFO] Install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    goto menu
)

echo [INFO] Building Docker images...
docker-compose build -q
echo [OK] Docker images built
echo.

echo [INFO] Starting services...
docker-compose up -d
echo [OK] Services started
echo.

timeout /t 3 >nul

echo [INFO] Testing API health...
curl -s http://localhost:8000/health >nul
if errorlevel 1 (
    echo [WARNING] API health check failed
    echo [INFO] Check logs with: docker-compose logs api
) else (
    echo [OK] API is healthy!
)

echo.
echo [OK] Docker deployment complete!
echo.
echo Access URLs:
echo   API: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo   UI: http://localhost:8501
echo.
echo Useful commands:
echo   View logs: docker-compose logs -f api
echo   Stop services: docker-compose down
echo.
pause
goto end

:test_api
echo.
echo [INFO] Testing API...

curl -s http://localhost:8000/health >nul
if errorlevel 1 (
    echo [ERROR] API is not running!
    echo [INFO] Start API first: python -m src.api.main
    pause
    goto menu
)

echo [OK] API is healthy!
echo.
echo [INFO] Testing job analysis...
curl -X POST http://localhost:8000/api/v1/jobs/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"job_id\": \"TEST-001\", \"job_title\": \"Senior Engineer\", \"job_text\": \"Need Python expert with 5+ years\"}"

echo.
pause
goto menu

:exit_script
echo [INFO] Goodbye! 👋
goto end

:end
endlocal
pause
