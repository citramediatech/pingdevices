===============================================================================
                       AUTO PING MONITOR v1.0
                    PT NexGen Solutions Asia
===============================================================================

Monitor status perangkat jaringan secara otomatis dan hasilkan gambar tangkapan
layar terminal bergaya macOS / Windows / Linux. Proyek ini portabel di Windows
(tanpa instalasi Python) serta dapat dijalankan di Linux dan macOS.


===============================================================================
FITUR UTAMA
===============================================================================

- Ping otomatis ke banyak perangkat berdasarkan daftar IP (iplist.txt)
- Output gambar seperti tangkapan layar terminal, lengkap dengan title bar
  sesuai sistem operasi
- Klasifikasi perangkat berdasarkan gedung dan kategori (CCTV, AP, Switch)
- Log duplikat IP untuk memudahkan audit jaringan
- Portabel di Windows - tinggal salin folder, tidak perlu instalasi Python
- Wrapper script siap pakai (run.cmd untuk Windows, run.sh untuk Linux/macOS)


===============================================================================
PRASYARAT
===============================================================================

Semua Sistem:
- Python 3.8+ (untuk menjalankan script utama)
  Untuk paket portabel Windows, Python sudah disertakan dalam folder python.
- Pillow - library Python untuk pembuatan gambar (akan diinstal otomatis
  oleh wrapper script jika belum ada)

Windows (Mode Portabel):
- Tidak ada prasyarat tambahan. Cukup jalankan run.cmd.


===============================================================================
STRUKTUR FOLDER
===============================================================================

pingdevices/
|
+-- python/            Python embeddable (khusus Windows portabel)
+-- ping_to_image.py   Script Python utama
+-- iplist.txt         Daftar IP perangkat
+-- run.cmd            Wrapper untuk Windows
+-- run.sh             Wrapper untuk Linux / macOS
+-- results/           Folder hasil (dibuat otomatis)
+-- logs.txt           Log duplikat IP (muncul jika ada)
+-- README.md          Dokumentasi


===============================================================================
INSTALASI & PENGGUNAAN
===============================================================================

---------------------------------
WINDOWS
---------------------------------

A. Menggunakan Python yang Sudah Terinstal di Sistem
----------------------------------------------------
1. Pastikan Python 3 sudah terinstal dan ditambahkan ke PATH
   (centang "Add Python to PATH" saat instalasi).
2. Buka Command Prompt di folder pingdevices, lalu instal Pillow:
   pip install pillow
3. Jalankan run.cmd (klik dua kali).
   Script akan memeriksa kelengkapan modul dan langsung menjalankan
   monitoring.

B. Mode Portabel (Tanpa Instalasi Python)
------------------------------------------
1. Dapatkan folder pingdevices yang sudah berisi folder python
   (Python embeddable + Pillow). Atau buat sendiri dengan mengikuti
   panduan portabel di bawah.
2. Salin seluruh folder ke komputer target (bisa lewat USB).
3. Jalankan run.cmd.
   Semua dependensi sudah berada di dalam folder, tidak perlu internet
   setelah persiapan pertama.


---------------------------------
LINUX / macOS
---------------------------------

1. Pastikan Python 3 terinstal
   (di macOS bisa lewat Homebrew: brew install python3).
2. Buka terminal di dalam folder pingdevices.
3. Beri izin eksekusi pada script wrapper (hanya sekali):
   chmod +x run.sh
4. Jalankan script:
   ./run.sh
   Script akan otomatis menginstal Pillow jika belum ada
   (menggunakan pip install --user), lalu menjalankan ping_to_image.py.
5. Setelah selesai, folder results akan terbuka secara otomatis.


===============================================================================
KONFIGURASI iplist.txt
===============================================================================

File iplist.txt berisi daftar perangkat yang akan di-ping.

PEMISAH YANG DIDUKUNG:
  | (pipe) , (koma) atau TAB

  Contoh:
  Camera-01|192.168.1.10
  Camera-02,192.168.1.11
  AP-Lobby    10.10.10.1

NAMA GEDUNG:
  Baris yang bukan IP valid dianggap nama gedung, hingga ditemukan
  nama gedung baru atau kategori.

  Contoh:
  #Gedung Utama

KATEGORI PERANGKAT:
  Ditandai dengan #CCTV, #AP, atau #SWITCH.
  Jika tidak ada, default adalah CCTV.

CONTOH LENGKAP:
--------------------------------------------------
#Gedung Utama
Camera-Gedung1|192.168.1.10
AP-Lantai1|10.10.10.1

#Gedung Kedua
#SWITCH
Switch-Core|172.16.0.1
--------------------------------------------------

Catatan: IP yang duplikat akan dicatat di logs.txt dan hanya perangkat
pertama yang diproses.


===============================================================================
OUTPUT
===============================================================================

Hasil monitoring disimpan di folder results/ dengan struktur:

results/
+-- CCTV/
|   +-- Gedung Utama/
|   |   +-- Camera-Gedung1.jpg
|   |   +-- ...
|   +-- Gedung Kedua/
+-- AP/
|   +-- ...
+-- SWITCH/
    +-- ...

Setiap gambar adalah tangkapan layar terminal dengan hasil ping 5 kali.
Warna HIJAU untuk reply, MERAH untuk timeout.


===============================================================================
MEMBUAT PAKET PORTABEL WINDOWS
===============================================================================

Jika Anda ingin membuat sendiri folder portabel tanpa bergantung Python
sistem:

1. Unduh Python Embeddable Package (versi 3.12.x atau 3.13.x) dari
   python.org/downloads/windows

2. Ekstrak isinya ke folder python di dalam pingdevices.

3. Buka file python313._pth (atau python312._pth) dengan Notepad.

4. Hilangkan tanda # pada baris #import site sehingga menjadi:
   import site

5. Simpan file.

6. Buka Command Prompt di folder python, lalu jalankan:
   python.exe -m ensurepip --upgrade
   python.exe -m pip install pillow

7. Verifikasi dengan:
   python.exe -c "import PIL; print('OK')"

   Jika muncul OK, folder pingdevices sudah portabel dan siap dipindahkan.


===============================================================================
TROUBLESHOOTING
===============================================================================

Masalah                                Solusi
-------------------------------------- --------------------------------------
python tidak dikenali di               Gunakan mode portabel, atau tambahkan
Command Prompt                         Python ke PATH saat instalasi.

ModuleNotFoundError:                   Install Pillow dengan pip install
No module named 'PIL'                  pillow atau jalankan run.cmd/run.sh
                                       yang akan menginstalnya otomatis.

Jendela run.cmd langsung menutup       Buka Command Prompt manual, arahkan
                                       ke folder, lalu jalankan run.cmd
                                       agar pesan error terlihat.

iplist.txt tidak ditemukan             Pastikan file tersebut berada di
                                       folder yang sama dengan
                                       ping_to_image.py.

Gagal membuat folder results           Jalankan dengan hak akses yang cukup,
                                       atau pindahkan folder ke lokasi yang
                                       dapat ditulis (misal Documents).


===============================================================================
KONTAK
===============================================================================

Dikembangkan oleh PT NexGen Solutions Asia

Untuk pertanyaan atau dukungan:

  Email   : djamal@nexgensolutions.asia
  Website : www.nexgensolutions.asia

===============================================================================