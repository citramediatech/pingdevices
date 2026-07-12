#!/usr/bin/env python3
import os
import re
import socket
import platform
from datetime import datetime
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# KONFIGURASI PATH RELATIF
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IP_FILE = os.path.join(BASE_DIR, "iplist.txt")
SAVE_FOLDER = os.path.join(BASE_DIR, "results/")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")

FONT_PATHS = [
    "/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf",
    "/System/Library/Fonts/SFMono-Regular.ttf", "/System/Library/Fonts/Supplemental/Courier New.ttf",
    "C:\\Windows\\Fonts\\Consola.ttf", "C:\\Windows\\Fonts\\Courier New.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
]

OS_TYPE = platform.system()
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
TIMEOUT_COLOR = (255, 80, 80)
TITLE_BG_COLOR = (43, 43, 43)
TITLE_TEXT_COLOR = (200, 200, 200)
PROMPT_COLOR = (120, 220, 120)

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
    TITLE_TEXT = f"{current_user}@{current_hostname} — zsh — 80x24"
elif OS_TYPE == 'Windows':
    LOCAL_PROMPT = f"PS C:\\Users\\{current_user}>"
    TITLE_TEXT = "Administrator: Windows PowerShell"
else:
    LOCAL_PROMPT = f"{current_user}@{current_hostname}:~$"
    TITLE_TEXT = f"{current_user}@{current_hostname}: ~ — bash — 80x24"

def get_text_size(draw, text, fnt):
    try:
        bbox = draw.textbbox((0, 0), text, font=fnt)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        return draw.textsize(text, font=fnt)

def safe_filename(name):
    if not name: return "Unknown"
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip() or "Unknown"

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
    draw.ellipse([(12, btn_y), (26, btn_y + 14)], fill=COLOR_CLOSE)
    draw.ellipse([(34, btn_y), (48, btn_y + 14)], fill=COLOR_MINIMIZE)
    draw.ellipse([(56, btn_y), (70, btn_y + 14)], fill=COLOR_MAXIMIZE)
    bbox = draw.textbbox((0, 0), TITLE_TEXT, font=title_font)
    text_x = (width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, (TITLE_HEIGHT - (bbox[3] - bbox[1])) // 2), TITLE_TEXT, fill=TITLE_TEXT_COLOR, font=title_font)

def draw_windows_title_bar(draw, width):
    draw.rectangle([(0, 0), (width, TITLE_HEIGHT)], fill=TITLE_BG_COLOR)
    draw.text((15, (TITLE_HEIGHT - TITLE_FONT_SIZE) // 2), TITLE_TEXT, fill=TITLE_TEXT_COLOR, font=title_font)

def draw_linux_title_bar(draw, width):
    draw.rectangle([(0, 0), (width, TITLE_HEIGHT)], fill=TITLE_BG_COLOR)
    btn_y = (TITLE_HEIGHT - 16) // 2
    btn_size = 16
    gap = 6
    draw.rectangle([(10, btn_y), (10 + btn_size, btn_y + btn_size)], fill=COLOR_CLOSE)
    draw.rectangle([(10 + btn_size + gap, btn_y), (10 + btn_size * 2 + gap, btn_y + btn_size)], fill=COLOR_MINIMIZE)
    draw.rectangle([(10 + (btn_size + gap) * 2, btn_y), (10 + btn_size * 3 + gap * 2, btn_y + btn_size)], fill=COLOR_MAXIMIZE)
    bbox = draw.textbbox((0, 0), TITLE_TEXT, font=title_font)
    text_x = (width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, (TITLE_HEIGHT - (bbox[3] - bbox[1])) // 2), TITLE_TEXT, fill=TITLE_TEXT_COLOR, font=title_font)

def draw_title_bar(draw, width):
    if OS_TYPE == 'Darwin': draw_macos_title_bar(draw, width)
    elif OS_TYPE == 'Windows': draw_windows_title_bar(draw, width)
    else: draw_linux_title_bar(draw, width)

# ==========================================
# EKSEKUSI PING (MENGGUNAKAN LIBRARY ping3)
# ==========================================
def execute_ping(dev_ip):
    results = []
    
    try:
        from ping3 import ping
    except ImportError:
        for _ in range(TOTAL_PING):
            results.append({'success': False, 'time_ms': None})
        stats_text = "Error: Library 'ping3' belum terinstall. Jalankan 'pip3 install ping3'"
        return results, stats_text

    # Lakukan ping 5 kali
    for _ in range(TOTAL_PING):
        # timeout 2 detik, unit milidetik
        rtt = ping(dev_ip, timeout=2, unit='ms')
        
        if rtt is not None and rtt > 0:
            results.append({'success': True, 'time_ms': round(rtt, 3)})
        else:
            results.append({'success': False, 'time_ms': None})

    # --- Hitung statistik ---
    stats_received = sum(1 for r in results if r['success'])
    stats_loss_percent = ((TOTAL_PING - stats_received) / TOTAL_PING) * 100
    times = [r['time_ms'] for r in results if r['success'] and r['time_ms'] is not None]

    stats_text = f"--- {dev_ip} ping statistics ---\n"
    stats_text += f"{TOTAL_PING} packets transmitted, {stats_received} received, {stats_loss_percent:.0f}% packet loss"
    if times:
        avg_time = sum(times) / len(times)
        stats_text += f"\nround-trip min/avg/max = {min(times):.3f}/{avg_time:.3f}/{max(times):.3f} ms"

    return results, stats_text

# ==========================================
# MEMBUAT GAMBAR HASIL PING
# ==========================================
def create_ping_image(dev_name, dev_ip, output_path):
    now = datetime.now()
    time_str = now.strftime("%a %b %d %H:%M:%S %Y")
    results, stats_text = execute_ping(dev_ip)

    output_lines = []
    for seq, res in enumerate(results):
        if res['success']:
            if OS_TYPE == 'Windows':
                text = f"Reply from {dev_ip}: bytes=32 time={res['time_ms']:.0f}ms TTL=128"
            else:
                text = f"64 bytes from {dev_ip}: icmp_seq={seq+1} ttl=64 time={res['time_ms']:.3f} ms"
            output_lines.append((text, TEXT_COLOR))
        else:
            if OS_TYPE == 'Windows':
                text = "Request timed out."
            else:
                text = f"Request timeout for icmp_seq {seq+1}"
            output_lines.append((text, TIMEOUT_COLOR))

    if stats_text:
        output_lines.append(("", TEXT_COLOR))
        for stat_line in stats_text.split('\n'):
            output_lines.append((stat_line, TEXT_COLOR))

    success_count = sum(1 for r in results if r['success'])
    terminal_lines = [
        (f"Last login: {time_str} on ttys000", TEXT_COLOR),
        (f"{LOCAL_PROMPT} ping {dev_ip}", PROMPT_COLOR),
    ] + output_lines + [(f"{LOCAL_PROMPT} ", PROMPT_COLOR)]

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
    draw_title_bar(draw, img_width)

    y = PADDING + TITLE_HEIGHT
    for text, color in all_rendered:
        draw.text((PADDING, y), text, fill=color, font=font)
        y += LINE_HEIGHT

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "JPEG", quality=95, optimize=True)
    except Exception as e:
        print(f"\n    [WARNING] Gagal simpan: {e}")

    return success_count > 0, success_count, TOTAL_PING - success_count

# ==========================================
# MEMBACA DAFTAR DEVICE
# ==========================================
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
                dev_name, dev_ip = parts[0].strip(), parts[1].strip()
            elif "," in line:
                parts = line.split(",", 1)
                dev_name, dev_ip = parts[0].strip(), parts[1].strip()
            elif "\t" in line:
                parts = line.split("\t", 1)
                dev_name, dev_ip = parts[0].strip(), parts[1].strip()

            if dev_name and dev_ip and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', dev_ip):
                if dev_ip in seen_ips:
                    duplicates.append({'gedung': current_gedung, 'name': dev_name, 'ip': dev_ip})
                else:
                    seen_ips.add(dev_ip)
                devices.append({'gedung': current_gedung, 'name': dev_name, 'ip': dev_ip, 'category': current_category})
                pending_name = None
            elif pending_name is not None:
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', line):
                    if line in seen_ips:
                        duplicates.append({'gedung': current_gedung, 'name': pending_name, 'ip': line})
                    else:
                        seen_ips.add(line)
                    devices.append({'gedung': current_gedung, 'name': pending_name, 'ip': line, 'category': current_category})
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
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    devices, duplicates = read_device_list(IP_FILE)
    if not devices:
        print("Tidak ada device ditemukan. Cek format file!")
        return

    if duplicates:
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
            if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
            print("\033[92m[INFO]\033[0m Tidak ditemukan duplikat IP.")
    else:
        if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
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