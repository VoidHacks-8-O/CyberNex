@echo off
setlocal enabledelayedexpansion

title OPERATION ABHEDYA-CHAKRA -- Offline Cyber Forensics Platform
echo ================================================================================
echo           OPERATION ABHEDYA-CHAKRA : OFFLINE FORENSICS & MULE DETECTION
echo ================================================================================
echo Mode: 100%% Local / Zero Internet Access Required
echo Engine: DuckDB Columnar B-Tree Index + FastAPI Backend
echo.

:: Navigate to script directory
cd /d "%~dp0"

:: Check Python installation
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in PATH.
    echo Please ensure Python 3.10+ is installed on this machine.
    pause
    exit /b 1
)

echo [1/3] Verifying local Python environment...
python -c "import duckdb, fastapi, uvicorn, pydantic, psutil; print('[OK] All required offline Python dependencies are present.')"
if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] Missing Python packages detected.
    echo Please make sure duckdb, fastapi, uvicorn, pydantic, psutil are installed in your offline Python environment.
    pause
    exit /b 1
)

echo [2/3] Checking local DuckDB database...
if exist "data\processed\abhedya_chakra.duckdb" (
    echo [OK] Local database file found: data\processed\abhedya_chakra.duckdb
) else (
    echo [INFO] Database will be initialized automatically from local dataset or schema.
)

echo [3/3] Launching local FastAPI forensics server on http://127.0.0.1:8000 ...
echo.
echo ================================================================================
echo   DASHBOARD URL : http://127.0.0.1:8000
echo   ALTERNATE FILE: %~dp0frontend\index.html
echo ================================================================================
echo   Press CTRL+C in this console window to stop the server.
echo.

:: Open default browser after a brief delay
start "" "http://127.0.0.1:8000"

:: Launch uvicorn locally
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000
