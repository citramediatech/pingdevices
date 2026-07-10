#!/bin/bash

INPUT="/Applications/pingdevices/iplist.txt"

if [ ! -f "$INPUT" ]; then
    echo "iplist.txt tidak ditemukan."
    exit 1
fi

FIRST=true

while read -r NAME && read -r IP
do

COMMAND="echo '$NAME ($IP)'; ping $IP"

if $FIRST; then
osascript <<EOF
tell application "Terminal"
    activate
    do script "$COMMAND"
end tell
EOF
FIRST=false
else
osascript <<EOF
tell application "Terminal"
    activate
    tell front window
        do script "$COMMAND" in selected tab
    end tell
end tell
EOF
fi

sleep 0.5

done < "$INPUT"