@echo off
title VoicePay Server
echo.
echo  Starting VoicePay local server...
echo.

:: Kill anything already using port 8080
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8080 "') do (
    taskkill /PID %%a /F >nul 2>&1
)

powershell.exe -ExecutionPolicy Bypass -File "%~dp0start-voicepay-server.ps1"
pause
