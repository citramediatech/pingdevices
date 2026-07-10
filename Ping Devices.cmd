@echo off
title PING MONITOR - PT NexGen Solutions Asia

cd /d "%~dp0"

if not exist "python\python.exe" (
    echo [ERROR] Python portable tidak ditemukan di folder python.
    pause
    exit /b
)

echo ================================================================
echo           PING MONITOR VERSI 1.0
echo    PT NexGen Solutions Asia
echo ================================================================
echo.

echo [INFO] Menjalankan script...
python\python.exe ping_to_image.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Script gagal. Kode error: %errorlevel%
    pause
    exit /b
)

echo.
echo ================================================================
echo    PROSES SELESAI!
echo ================================================================
echo.
set /p enterKey="Tekan [ENTER] untuk membuka folder hasil..."
if exist "results" (
    explorer "results"
) else (
    echo Folder results belum dibuat.
    pause
)