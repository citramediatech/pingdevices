#!/bin/bash
clear
echo -e "\033[1;36m================================================================\033[0m"
echo -e "\033[1;36m                    AUTO PING MONITOR v1.0\033[0m"
echo -e "\033[1;36m================================================================\033[0m"
echo ""
echo -e "\033[1;33m[INFO]\033[0m Menjalankan script ping ke database..."
echo ""

# Deteksi OS untuk perintah python yang benar
if [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD="python3"
    OPEN_CMD="open"
else
    PYTHON_CMD="python3"
    OPEN_CMD="xdg-open"
fi

$PYTHON_CMD "$(dirname "$0")/ping_to_image.py"

echo ""
echo -e "\033[1;32m================================================================\033[0m"
echo -e "\033[1;32m   PROSES SELESAI!\033[0m"
echo -e "\033[1;32m================================================================\033[0m"
echo ""
read -p "Tekan [ENTER] untuk membuka folder hasil... " enterKey
$OPEN_CMD "$(dirname "$0")/results"