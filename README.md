Jika Anda ingin seperti di Windows (tidak perlu install Python & modul secara global), Anda bisa menggunakan Python virtual environment di dalam folder proyek. Ikuti langkah berikut di terminal, di folder pingdevices:
# Buat virtual environment (sekali saja)
python3 -m venv venv

# Aktifkan dan install Pillow
source venv/bin/activate
pip install pillow
deactivate
