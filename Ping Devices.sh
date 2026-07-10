#!/bin/bash
clear

# ==========================================
# Warna
# ==========================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}           PING MONITOR v1.0 - PT NexGen Solutions Asia${NC}"
echo -e "${CYAN}================================================================${NC}"
echo ""

# ==========================================
# Deteksi OS & tentukan perintah
# ==========================================
if [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD="python3"
    OPEN_CMD="open"
else
    PYTHON_CMD="python3"
    OPEN_CMD="xdg-open"
fi

# ==========================================
# Cek python3
# ==========================================
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 tidak ditemukan."
    echo "        Install Python 3 terlebih dahulu (https://python.org)"
    read -p "Tekan Enter untuk keluar..."
    exit 1
fi

# ==========================================
# Cek keberadaan script Python
# ==========================================
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_FILE="$SCRIPT_DIR/ping_to_image.py"
if [ ! -f "$PYTHON_FILE" ]; then
    echo -e "${RED}[ERROR]${NC} File ping_to_image.py tidak ditemukan di $SCRIPT_DIR"
    read -p "Tekan Enter untuk keluar..."
    exit 1
fi

# ==========================================
# Cek & install Pillow jika perlu
# ==========================================
echo -e "${YELLOW}[INFO]${NC} Memeriksa modul Pillow..."
$PYTHON_CMD -c "import PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Pillow belum terinstall. Menginstall otomatis..."
    $PYTHON_CMD -m pip install --user pillow
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Gagal menginstall Pillow."
        echo "        Coba jalankan manual: $PYTHON_CMD -m pip install --user pillow"
        read -p "Tekan Enter untuk keluar..."
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Pillow berhasil diinstall."
else
    echo -e "${GREEN}[OK]${NC} Pillow sudah terinstall."
fi
echo ""

# ==========================================
# Jalankan script Python
# ==========================================
echo -e "${YELLOW}[INFO]${NC} Menjalankan ping_to_image.py..."
$PYTHON_CMD "$PYTHON_FILE"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Script Python berhenti dengan kode error $EXIT_CODE."
    echo "        Periksa apakah iplist.txt ada dan formatnya benar."
    read -p "Tekan Enter untuk keluar..."
    exit $EXIT_CODE
fi

echo ""
echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}   PROSES SELESAI!${NC}"
echo -e "${GREEN}================================================================${NC}"
echo ""
read -p "Tekan [ENTER] untuk membuka folder hasil... " enterKey

# Buka folder hasil
if [ -d "$SCRIPT_DIR/results" ]; then
    $OPEN_CMD "$SCRIPT_DIR/results"
else
    echo -e "${YELLOW}[INFO]${NC} Folder results belum dibuat."
    read -p "Tekan Enter untuk keluar..."
fi
