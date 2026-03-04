@echo off
REM Auto-commit and push helper batch script for Windows
REM Usage: commit.bat [message] [--push]

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Checking git status...
git status --short > nul
if errorlevel 1 (
    echo Error: Not a git repository or git not found
    exit /b 1
)

git status --short | find /v "" > nul
if errorlevel 1 (
    echo No changes to commit
    exit /b 0
)

echo.
echo Changes detected:
git status --short

echo.
echo Staging changes...
git add -A

if errorlevel 1 (
    echo Error: Failed to stage changes
    exit /b 1
)

REM Create commit message
if "%1"=="" (
    for /f "tokens=2-4 delims=/ " %%%%a in ('date /t') do (set mydate=%%%%c-%%%%a-%%%%b)
    for /f "tokens=1-2 delims=/:" %%%%a in ('time /t') do (set mytime=%%%%a:%%%%b)
    set message=chore: Auto-commit - !mydate! !mytime!
) else (
    set message=%1
    shift
)

echo.
echo Creating commit: "!message!"
git commit -m "!message!"

if errorlevel 1 (
    echo Error: Failed to create commit
    exit /b 1
)

echo Commit successful!

REM Check for --push flag
if "%1"=="--push" (
    echo.
    echo Pushing to origin/main...
    git push -u origin main
    if errorlevel 1 (
        echo Error: Failed to push
        exit /b 1
    )
    echo Push successful!
) else (
    echo.
    echo Run with --push flag to push changes to remote
    echo Usage: commit.bat [message] --push
)

endlocal
exit /b 0
