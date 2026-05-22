@echo off
chcp 65001 > nul
title Thiep Cuoi - Mai Em ^& Tien Toan
cd /d "%~dp0"

echo.
echo ===============================================
echo   Thiep Cuoi - Mai Em ^& Tien Toan
echo ===============================================
echo.
echo  Server: http://localhost:8000
echo  Browser se tu mo trong 2 giay...
echo.
echo  Nhan Ctrl+C de dung server.
echo  Dong cua so nay = dung server.
echo ===============================================
echo.

start "" "http://localhost:8000"
python -m http.server 8000

pause
