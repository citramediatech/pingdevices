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
echo -e "${CYAN}           PING MONITOR v1.1 - PT NexGen Solutions Asia${NC}"
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
# Cek keberadaan script Python (prioritas: macOS version)
# ==========================================
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$SCRIPT_DIR/ping_to_image_macOS.py" ]; then
    PYTHON_FILE="$SCRIPT_DIR/ping_to_image_macOS.py"
elif [ -f "$SCRIPT_DIR/ping_to_image.py" ]; then
    PYTHON_FILE="$SCRIPT_DIR/ping_to_image.py"
else
    echo -e "${RED}[ERROR]${NC} Tidak ditemukan ping_to_image_macOS.py atau ping_to_image.py"
    echo "        Pastikan file script Python ada di $SCRIPT_DIR"
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
# JALANKAN PYTHON
# ==========================================
echo -e "${YELLOW}[INFO]${NC} Menjalankan $PYTHON_FILE..."

TMP_OUTPUT=$(mktemp)
$PYTHON_CMD "$PYTHON_FILE" 2>&1 | tee "$TMP_OUTPUT"
EXIT_CODE=${PIPESTATUS[0]}

SAVE_FOLDER=$(grep -o "Folder hasil: .*" "$TMP_OUTPUT" | tail -1 | sed 's/Folder hasil: //')
rm "$TMP_OUTPUT"

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Script Python berhenti dengan kode error $EXIT_CODE."
    echo "        Periksa apakah file IP yang dipilih valid dan formatnya benar."
    read -p "Tekan Enter untuk keluar..."
    exit $EXIT_CODE
fi

if [ -z "$SAVE_FOLDER" ]; then
    SAVE_FOLDER="$SCRIPT_DIR/results"
    echo -e "${YELLOW}[INFO]${NC} Folder hasil tidak terdeteksi, menggunakan default: $SAVE_FOLDER"
fi

echo ""
echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}   PROSES SELESAI!${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "   Folder hasil: ${CYAN}$SAVE_FOLDER${NC}"
echo ""

# ==========================================
# Tanyakan untuk membuka folder
# ==========================================
read -p "Tekan [ENTER] untuk membuka folder hasil... " openKey

if [ -d "$SAVE_FOLDER" ]; then
    $OPEN_CMD "$SAVE_FOLDER"
else
    echo -e "${YELLOW}[INFO]${NC} Folder $SAVE_FOLDER belum dibuat (mungkin belum ada gambar)."
fi

echo ""
read -p "Tekan [ENTER] untuk menutup terminal... " closeKey

# ==========================================
# Tutup jendela Terminal yang sedang aktif
# ==========================================
osascript -e 'tell application "Terminal" to close front window' 2>/dev/null
exit 0