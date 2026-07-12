@echo off
title PING MONITOR v1.1 - PT NexGen Solutions Asia
cd /d "%~dp0"

set RED=[91m
set GREEN=[92m
set YELLOW=[93m
set CYAN=[96m
set NC=[0m

echo %CYAN%================================================================%NC%
echo %CYAN%           PING MONITOR v1.1 - PT NexGen Solutions Asia%NC%
echo %CYAN%================================================================%NC%
echo.

if not exist "python\python.exe" (
    echo %RED%[ERROR]%NC% Python portable tidak ditemukan di folder python.
    echo        Pastikan folder python berisi python.exe.
    pause
    exit /b 1
)

echo %YELLOW%[INFO]%NC% Memeriksa modul Pillow dan ping3...
python\python.exe -c "import PIL; import ping3" >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%[WARNING]%NC% Modul belum terinstall. Menginstall otomatis...
    python\python.exe -m pip install --user pillow ping3
    if %errorlevel% neq 0 (
        echo %RED%[ERROR]%NC% Gagal menginstall modul.
        echo        Coba jalankan manual: python\python.exe -m pip install pillow ping3
        pause
        exit /b 1
    )
    echo %GREEN%[OK]%NC% Modul berhasil diinstall.
) else (
    echo %GREEN%[OK]%NC% Pillow dan ping3 sudah terinstall.
)
echo.

echo %YELLOW%[INFO]%NC% Menjalankan ping_to_image.py...
echo.
python\python.exe ping_to_image.py
set EXIT_CODE=%errorlevel%

if %EXIT_CODE% neq 0 (
    echo.
    echo %RED%[ERROR]%NC% Script Python berhenti dengan kode error %EXIT_CODE%.
    echo        Periksa apakah file IP yang dipilih valid dan formatnya benar.
    pause
    exit /b %EXIT_CODE%
)

set SAVE_FOLDER=

if exist "last_folder.txt" (
    for /f "usebackq delims=" %%a in ("last_folder.txt") do set "SAVE_FOLDER=%%a"
    del "last_folder.txt"
)

if "%SAVE_FOLDER%"=="" (
    set SAVE_FOLDER=%~dp0results
    echo %YELLOW%[INFO]%NC% Folder hasil tidak terdeteksi, menggunakan default: %SAVE_FOLDER%
)

echo.
echo %GREEN%================================================================%NC%
echo %GREEN%   PROSES SELESAI!%NC%
echo %GREEN%================================================================%NC%
echo    Folder hasil: %CYAN%%SAVE_FOLDER%%NC%
echo.

set /p "openKey=Tekan [ENTER] untuk membuka folder hasil... "

if exist "%SAVE_FOLDER%" (
    echo Membuka folder hasil...
    start "" "%SAVE_FOLDER%"
    echo Folder hasil sudah dibuka.
) else (
    echo %YELLOW%[INFO]%NC% Folder %SAVE_FOLDER% belum ditemukan.
    echo        Kemungkinan script Python tidak membuat folder karena tidak ada gambar yang tersimpan.
)

echo.
set /p "closeKey=Tekan [ENTER] untuk menutup terminal... "
exit