#!/usr/bin/env python3
import subprocess
import os
import re
import socket
import platform
from datetime import datetime
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# KONFIGURASI PATH RELATIF (AGAR PORTABLE)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IP_FILE = os.path.join(BASE_DIR, "iplist.txt")
SAVE_FOLDER = os.path.join(BASE_DIR, "results/")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")

FONT_PATHS = [
    "/System/Library/Fonts/Menlo.ttc",
    "/Library/Fonts/Menlo.ttc", 
    "/System/Library/Fonts/Monaco.ttf",
    "/System/Library/Fonts/SFMono-Regular.ttf",
    "/System/Library/Fonts/Supplemental/Courier New.ttf",
    "C:\\Windows\\Fonts\\Consola.ttf",
    "C:\\Windows\\Fonts\\Courier New.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]

OS_TYPE = platform.system()

# ==========================================
# KONFIGURASI WARNA & UKURAN
# ==========================================
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)    # PUTIH (untuk Reply)
TIMEOUT_COLOR = (255, 80, 80)   # MERAH (untuk Timeout)
TITLE_BG_COLOR = (43, 43, 43)
TITLE_TEXT_COLOR = (200, 200, 200)

FONT_SIZE = 18
TITLE_FONT_SIZE = 13
PADDING = 30
LINE_HEIGHT = 28
TITLE_HEIGHT = 38
TOTAL_PING = 5

if OS_TYPE == 'Darwin':
    COLOR_CLOSE, COLOR_MINIMIZE, COLOR_MAXIMIZE = (255, 95, 87), (255, 189, 46), (39, 201, 63)
elif OS_TYPE == 'Windows':
    COLOR_CLOSE, COLOR_MINIMIZE, COLOR_MAXIMIZE = (255, 80, 80), (220, 220, 220), (220, 220, 220)
else:
    COLOR_CLOSE, COLOR_MINIMIZE, COLOR_MAXIMIZE = (255, 80, 80), (255, 200, 80), (80, 200, 80)

def load_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

font = load_font(FONT_SIZE)
title_font = load_font(TITLE_FONT_SIZE)

def get_current_user():
    try:
        return os.getlogin()
    except:
        return os.environ.get('USER', os.environ.get('USERNAME', 'user'))

current_user = get_current_user()
current_hostname = socket.gethostname().split('.')[0]

if OS_TYPE == 'Darwin':
    LOCAL_PROMPT = f"{current_user}@{current_hostname} ~ %"
    TITLE_TEXT = f"{current_user}@{current_hostname} — -zsh — 80x24"
elif OS_TYPE == 'Windows':
    LOCAL_PROMPT = f"PS C:\\Users\\{current_user}>"
    TITLE_TEXT = f"Administrator: Windows PowerShell"
else:
    LOCAL_PROMPT = f"{current_user}@{current_hostname}:~$"
    TITLE_TEXT = f"{current_user}@{current_hostname}:~ — -bash — 80x24"

def get_text_size(draw, text, fnt):
    try:
        bbox = draw.textbbox((0, 0), text, font=fnt)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        return draw.textsize(text, font=fnt)

def safe_filename(name):
    if not name: return "Unknown"
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    return name.strip() if name.strip() else "Unknown"

def wrap_text(text, draw, fnt, max_width):
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split()
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            w, _ = get_text_size(draw, test_line, fnt)
            if w <= max_width:
                current_line = test_line
            else:
                if current_line: lines.append(current_line)
                current_line = word
        if current_line: lines.append(current_line)
    return lines

def draw_macos_title_bar(draw, width):
    draw.rectangle([(0, 0), (width, TITLE_HEIGHT)], fill=TITLE_BG_COLOR)
    btn_y = (TITLE_HEIGHT - 14) // 2
    draw.ellipse([(10, btn_y), (24, btn_y + 14)], fill=COLOR_CLOSE)
    draw.ellipse([(32, btn_y), (46, btn_y + 14)], fill=COLOR_MINIMIZE)
    draw.ellipse([(54, btn_y), (68, btn_y + 14)], fill=COLOR_MAXIMIZE)
    bbox = draw.textbbox((0, 0), TITLE_TEXT, font=title_font)
    text_x = (width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, (TITLE_HEIGHT - TITLE_FONT_SIZE) // 2 - 1), TITLE_TEXT, fill=TITLE_TEXT_COLOR, font=title_font)

def draw_windows_title_bar(draw, width):
    draw.rectangle([(0, 0), (width, TITLE_HEIGHT)], fill=TITLE_BG_COLOR)
    draw.rectangle([(width - 150, 0), (width - 100, TITLE_HEIGHT)], fill=TITLE_BG_COLOR)
    draw.line([(width - 140, TITLE_HEIGHT // 2), (width - 110, TITLE_HEIGHT // 2)], fill="white", width=2)
    draw.rectangle([(width - 100, 0), (width - 50, TITLE_HEIGHT)], fill=TITLE_BG_COLOR)
    draw.rectangle([(width - 90, 8), (width - 60, TITLE_HEIGHT - 8)], outline="white", width=2)
    draw.rectangle([(width - 50, 0), (width, TITLE_HEIGHT)], fill=COLOR_CLOSE)
    draw.text((width - 38, 8), "X", fill="white", font=title_font)
    draw.text((15, (TITLE_HEIGHT - TITLE_FONT_SIZE) // 2 - 1), TITLE_TEXT, fill=TITLE_TEXT_COLOR, font=title_font)

def draw_linux_title_bar(draw, width):
    draw.rectangle([(0, 0), (width, TITLE_HEIGHT)], fill=TITLE_BG_COLOR)
    btn_y = (TITLE_HEIGHT - 18) // 2
    draw.rectangle([(10, btn_y), (28, btn_y + 18)], fill=COLOR_CLOSE)
    draw.rectangle([(34, btn_y), (52, btn_y + 18)], fill=COLOR_MINIMIZE)
    draw.rectangle([(58, btn_y), (76, btn_y + 18)], fill=COLOR_MAXIMIZE)
    bbox = draw.textbbox((0, 0), TITLE_TEXT, font=title_font)
    text_x = (width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, (TITLE_HEIGHT - TITLE_FONT_SIZE) // 2 - 1), TITLE_TEXT, fill=TITLE_TEXT_COLOR, font=title_font)

# ==========================================
# EKSEKUSI PING (DIPERBAIKI UNTUK WINDOWS)
# ==========================================
def execute_ping(dev_ip):
    reply_count = 0
    avg_time = 0.0
    stats_text = ""
    
    if OS_TYPE == 'Windows':
        cmd = ["ping", "-n", str(TOTAL_PING), "-w", "2000", dev_ip]
    else:
        cmd = ["ping", "-c", str(TOTAL_PING), "-W", "2", dev_ip]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        stdout = result.stdout
        
        # Debug print
        print(f"\n--- DEBUG PING {dev_ip} ---")
        for line in stdout.splitlines():
            print(f"  {line}")
        print("-------------------------")

        # Parsing jumlah reply (Windows vs Unix)
        if OS_TYPE == 'Windows':
            # Contoh: "Packets: Sent = 5, Received = 5, Lost = 0 (0% loss)"
            match = re.search(r'Received\s*=\s*(\d+)', stdout)
            if match:
                reply_count = int(match.group(1))
            # RTT: "Minimum = 0ms, Maximum = 1ms, Average = 0ms"
            match_avg = re.search(r'Average\s*=\s*(\d+)ms', stdout)
            if match_avg:
                avg_time = float(match_avg.group(1))
        else:
            # Unix style
            rx_match = re.search(r'(\d+)\s+(?:packets?\s+)?received', stdout, re.IGNORECASE)
            if rx_match:
                reply_count = int(rx_match.group(1))
            rtt_avg_match = re.search(r'(?:round-trip|rtt)\s+min/avg/max/[a-z]+\s*=\s*[\d.]+/([\d.]+)/', stdout, re.IGNORECASE)
            if rtt_avg_match:
                avg_time = float(rtt_avg_match.group(1))

        # Ambil statistik lengkap untuk ditampilkan
        if OS_TYPE == 'Windows':
            lines = stdout.splitlines()
            stats_lines = []
            in_stats = False
            for line in lines:
                if "Ping statistics" in line:
                    in_stats = True
                if in_stats:
                    stats_lines.append(line)
                    if "Average" in line:
                        break
            stats_text = "\n".join(stats_lines).strip() if stats_lines else f"--- {dev_ip} ping statistics ---\n{TOTAL_PING} packets transmitted, {reply_count} packets received"
        else:
            stats_lines = []
            in_stats = False
            for line in stdout.splitlines():
                if "ping statistics" in line or "---" in line:
                    in_stats = True
                if in_stats:
                    stats_lines.append(line)
                    if "packet loss" in line and "transmitted" in line:
                        break
            stats_text = "\n".join(stats_lines).strip() if stats_lines else f"--- {dev_ip} ping statistics ---\n{TOTAL_PING} packets transmitted, {reply_count} packets received"

    except subprocess.TimeoutExpired:
        reply_count = 0
        stats_text = f"--- {dev_ip} ping statistics ---\n{TOTAL_PING} packets transmitted, 0 packets received, 100% packet loss"
    except Exception as e:
        reply_count = 0
        stats_text = f"Error: {str(e)}"

    return reply_count, avg_time, stats_text

def create_ping_image(dev_name, dev_ip, output_path):
    now = datetime.now()
    time_str = now.strftime("%a %b %d %H:%M:%S %Y")

    reply_count, avg_time, stats_text = execute_ping(dev_ip)

    output_lines = []
    for seq in range(TOTAL_PING):
        if seq < reply_count:
            if OS_TYPE == 'Windows':
                text = f"Reply from {dev_ip}: bytes=32 time={avg_time:.0f}ms TTL=128"
            else:
                text = f"64 bytes from {dev_ip}: icmp_seq={seq} ttl=64 time={avg_time:.3f} ms"
            output_lines.append((text, TEXT_COLOR))
        else:
            if OS_TYPE == 'Windows':
                text = "Request timed out."
            else:
                text = f"Request timeout for icmp_seq {seq}"
            output_lines.append((text, TIMEOUT_COLOR))

    if stats_text:
        output_lines.append(("", TEXT_COLOR))
        for stat_line in stats_text.split('\n'):
            output_lines.append((stat_line, TEXT_COLOR))

    is_success = reply_count > 0

    terminal_lines = [
        (f"Last login: {time_str} on ttys000", TEXT_COLOR),
        (f"{LOCAL_PROMPT} ping {dev_ip}", TEXT_COLOR),
    ]
    terminal_lines.extend(output_lines)
    terminal_lines.append((f"{LOCAL_PROMPT}", TEXT_COLOR))

    temp_img = Image.new("RGB", (1, 1), BG_COLOR)
    temp_draw = ImageDraw.Draw(temp_img)
    all_rendered = []
    max_width = 0

    for text, color in terminal_lines:
        wrapped = wrap_text(text, temp_draw, font, 1200)
        for wl in wrapped:
            all_rendered.append((wl, color))
            w, _ = get_text_size(temp_draw, wl, font)
            max_width = max(max_width, w)

    img_width = max(max_width + (PADDING * 2), 450)
    img_height = (len(all_rendered) * LINE_HEIGHT) + (PADDING * 2) + TITLE_HEIGHT

    img = Image.new("RGB", (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    if OS_TYPE == 'Darwin':
        draw_macos_title_bar(draw, img_width)
    elif OS_TYPE == 'Windows':
        draw_windows_title_bar(draw, img_width)
    else:
        draw_linux_title_bar(draw, img_width)

    y = PADDING + TITLE_HEIGHT
    for text, color in all_rendered:
        draw.text((PADDING, y), text, fill=color, font=font)
        y += LINE_HEIGHT

    try:
        img.save(output_path, "JPEG", quality=95, optimize=True)
    except Exception as e:
        print(f"Warning: Gagal simpan - {e}")

    return is_success, reply_count, TOTAL_PING - reply_count

def read_device_list(filepath):
    devices = []
    duplicates = []
    seen_ips = set()
    current_gedung = "Unknown"
    current_category = "CCTV"
    pending_name = None

    if not os.path.exists(filepath):
        print(f"Error: File tidak ditemukan - {filepath}")
        return devices, duplicates

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue

            if line.startswith("#"):
                clean_line = line.lstrip('#').strip().upper()
                if clean_line == "CCTV":
                    current_category = "CCTV"
                elif clean_line == "AP":
                    current_category = "AP"
                elif clean_line == "SWITCH":
                    current_category = "SWITCH"
                
                gedung_text = line.lstrip('#').strip()
                if gedung_text and gedung_text.upper() not in ["CCTV", "AP", "SWITCH"] and len(gedung_text) > 2:
                    current_gedung = gedung_text
                continue

            dev_name = dev_ip = None
            if "|" in line:
                parts = line.split("|", 1)
                if len(parts) == 2:
                    dev_name, dev_ip = parts[0].strip(), parts[1].strip()
            elif "," in line:
                parts = line.split(",", 1)
                if len(parts) == 2:
                    dev_name, dev_ip = parts[0].strip(), parts[1].strip()
            elif "\t" in line:
                parts = line.split("\t", 1)
                if len(parts) == 2:
                    dev_name, dev_ip = parts[0].strip(), parts[1].strip()

            if dev_name and dev_ip and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', dev_ip):
                if dev_ip in seen_ips:
                    duplicates.append({
                        'gedung': current_gedung,
                        'name': dev_name,
                        'ip': dev_ip
                    })
                else:
                    seen_ips.add(dev_ip)

                devices.append({
                    'gedung': current_gedung,
                    'name': dev_name,
                    'ip': dev_ip,
                    'category': current_category
                })
                pending_name = None
            elif pending_name is not None:
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', line):
                    if line in seen_ips:
                        duplicates.append({
                            'gedung': current_gedung,
                            'name': pending_name,
                            'ip': line
                        })
                    else:
                        seen_ips.add(line)

                    devices.append({
                        'gedung': current_gedung,
                        'name': pending_name,
                        'ip': line,
                        'category': current_category
                    })
                    pending_name = None
                else:
                    pending_name = line
            else:
                if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', line):
                    pending_name = line

    return devices, duplicates

# ==========================================
# MAIN
# ==========================================
def main():
    # Buat folder results jika belum ada
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    devices, duplicates = read_device_list(IP_FILE)
    if not devices:
        print("Tidak ada device ditemukan. Cek format file!")
        return

    # Log Duplikat
    if duplicates:
        try:
            grouped = defaultdict(list)
            for dup in duplicates:
                grouped[dup['ip']].append(dup)
            
            real_duplicates = {ip: items for ip, items in grouped.items() if len(items) > 1}
            
            if real_duplicates:
                with open(LOG_FILE, 'w', encoding='utf-8') as f:
                    f.write("=" * 60 + "\n")
                    f.write(f"DUPLIKAT IP DITEMUKAN PADA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for ip, items in real_duplicates.items():
                        gedung1 = items[0]['gedung'].replace("Gedung ", "").strip()
                        line = f"{ip} Digunkan Device {items[0]['name']} (Gedung {gedung1})"
                        
                        for item in items[1:]:
                            gedung_n = item['gedung'].replace("Gedung ", "").strip()
                            line += f", Duplicate Device {item['name']} (Gedung {gedung_n})"
                        
                        f.write(line + "\n")
                    
                    f.write("\n" + "=" * 60 + "\n")
                
                print(f"\033[93m[WARNING]\033[0m Ditemukan {len(real_duplicates)} IP duplikat. Lihat log di {LOG_FILE}")
            else:
                if os.path.exists(LOG_FILE):
                    os.remove(LOG_FILE)
                print("\033[92m[INFO]\033[0m Tidak ditemukan duplikat IP.")
        except Exception as e:
            print(f"\033[91m[ERROR]\033[0m Gagal menulis log duplikat: {e}")
    else:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        print("\033[92m[INFO]\033[0m Tidak ditemukan duplikat IP.")

    success_count = 0
    partial_count = 0
    fail_count = 0
    total = len(devices)

    print(f"Device dipakai : {LOCAL_PROMPT}")
    print(f"Total target  : {total} device")
    print("=" * 65)

    for idx, device in enumerate(devices, 1):
        gedung = device['gedung']
        name = device['name']
        ip = device['ip']
        cat = device['category']

        folder_path = os.path.join(SAVE_FOLDER, safe_filename(cat), safe_filename(gedung))
        os.makedirs(folder_path, exist_ok=True)

        save_path = os.path.join(folder_path, f"{safe_filename(name).replace(' ', '_')}.jpg")

        print(f"[{idx:3d}/{total}] ", end="", flush=True)

        try:
            is_ok, reply_cnt, timeout_cnt = create_ping_image(name, ip, save_path)
        except Exception as e:
            print(f"\033[91m{gedung} [{name}-{cat}-ERROR]\033[0m -> {e}")
            fail_count += 1
            continue

        if reply_cnt == TOTAL_PING:
            success_count += 1
            print(f"\033[92m{gedung} [{name}-{cat}-OK {reply_cnt}/{TOTAL_PING}]\033[0m")
        elif reply_cnt > 0:
            partial_count += 1
            print(f"\033[93m{gedung} [{name}-{cat}-PARTIAL {reply_cnt}/{TOTAL_PING}]\033[0m")
        else:
            fail_count += 1
            print(f"\033[91m{gedung} [{name}-{cat}-OFF 0/{TOTAL_PING}]\033[0m")

    print("=" * 65)
    print(f"\033[96mSelesai!\033[0m")
    print(f"  \033[92m● Online  : {success_count}\033[0m ( 5/5 Reply )")
    print(f"  \033[93m● Partial : {partial_count}\033[0m ( Loss di tengah )")
    print(f"  \033[91m● Offline : {fail_count}\033[0m ( 0/5 Reply )")
    print(f"\nFolder hasil: {SAVE_FOLDER}")

if __name__ == "__main__":
    main()