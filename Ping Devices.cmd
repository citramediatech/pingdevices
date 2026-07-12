@echo off
title PING DEVICES MONITOR v1.1 - PT NexGen Solutions Asia by Qomaruddin Djamal
cd /d "%~dp0"

echo ================================================================
echo        PING DEVICES MONITOR v1.1 - PT NexGen Solutions Asia
echo ================================================================
echo.

REM ================================================================
REM 1. CEK & DOWNLOAD PYTHON (JIKA BELUM ADA)
REM ================================================================
if not exist "python\python.exe" (
    echo.
    echo [INFO] Python portable tidak ditemukan di folder python.
    echo [INFO] Mengunduh Python Embeddable 3.13.0...
    curl -L -o python.zip https://www.python.org/ftp/python/3.13.0/python-3.13.0-embed-amd64.zip

    if not exist "python.zip" (
        echo.
        echo [ERROR] Gagal mengunduh Python.
        echo        Pastikan internet terhubung.
        pause
        exit /b 1
    )

    echo [INFO] Mengekstrak Python...
    powershell -Command "Expand-Archive -Path python.zip -DestinationPath .\python"
    del python.zip

    echo [INFO] Mengaktifkan import site...
    for /f "delims=" %%i in ('dir /b python\python*._pth 2^>nul') do (
        powershell -Command "(Get-Content 'python\%%i') -replace '#import site', 'import site' | Set-Content 'python\%%i'"
    )
    echo [OK] Python siap.
)
echo.

REM ================================================================
REM 2. CEK & INSTALL PIP (JIKA BELUM ADA)
REM ================================================================
if not exist "python\Scripts\pip.exe" (
    echo [INFO] Mengunduh get-pip.py...
    curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py --ssl-no-revoke

    if not exist "get-pip.py" (
        echo.
        echo [ERROR] Gagal mengunduh get-pip.py.
        echo        Pastikan internet terhubung.
        pause
        exit /b 1
    )

    echo [INFO] Menginstall pip...
    python\python.exe get-pip.py

    if not exist "python\Scripts\pip.exe" (
        echo.
        echo [ERROR] Gagal menginstall pip.
        pause
        exit /b 1
    )
    del get-pip.py
    echo [OK] Pip siap.
)
echo.

REM ================================================================
REM 3. INSTALL MODUL PILLOW (HANYA CEK FOLDER PIL)
REM ================================================================
if not exist "python\Lib\site-packages" mkdir "python\Lib\site-packages"

if not exist "python\Lib\site-packages\PIL" (
    echo [INFO] Menginstall Pillow dan ping3...
    python\python.exe -m pip install --target "python\Lib\site-packages" pillow ping3

    if not exist "python\Lib\site-packages\PIL" (
        echo.
        echo [ERROR] Gagal menginstall Pillow.
        echo        Coba manual: python\python.exe -m pip install --target "python\Lib\site-packages" pillow ping3
        pause
        exit /b 1
    )
    echo [OK] Modul terinstall.
) else (
    echo [OK] Pillow sudah ada.
)
echo.

REM ================================================================
REM 4. BERSIHKAN LAYAR & JALANKAN PYTHON SCRIPT
REM ================================================================
cls
echo ================================================================
echo        PING DEVICES MONITOR v1.1 - PT NexGen Solutions Asia
echo ================================================================
echo.
echo [INFO] Menjalankan ping_to_image.py...
echo.
python\python.exe ping_to_image.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Script Python gagal. Kode error: %errorlevel%
    echo        Periksa apakah iplist.txt ada dan formatnya benar.
    pause
    exit /b %errorlevel%
)

REM ================================================================
REM 5. BACA FOLDER HASIL
REM ================================================================
set SAVE_FOLDER=
if exist "last_folder.txt" (
    for /f "usebackq delims=" %%a in ("last_folder.txt") do set "SAVE_FOLDER=%%a"
    del "last_folder.txt"
)

if "%SAVE_FOLDER%"=="" (
    set SAVE_FOLDER=%~dp0results
    echo [INFO] Folder hasil tidak terdeteksi, menggunakan default: %SAVE_FOLDER%
)

echo.
echo ================================================================
echo    PROSES SELESAI!
echo ================================================================
echo    Folder hasil: %SAVE_FOLDER%
echo.

set /p "openKey=Tekan [ENTER] untuk membuka folder hasil... "

if exist "%SAVE_FOLDER%" (
    echo Membuka folder hasil...
    start "" "%SAVE_FOLDER%"
    echo Folder hasil sudah dibuka.
) else (
    echo [INFO] Folder %SAVE_FOLDER% belum ditemukan.
)

echo.
set /p "closeKey=Tekan [ENTER] untuk menutup terminal... "
exit