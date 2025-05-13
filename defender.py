import subprocess
import re
import time
from datetime import datetime

# Regex to catch IPs from kernel SYN flood logs
log_pattern = re.compile(r'SYN FLOOD DROPPED.*SRC=([\d.]+)')

# Track banned IPs with timestamps
banned_ips = {}
BAN_DURATION = 3600  # 1 hour

def ban_ip(ip):
    if ip not in banned_ips:
        print(f"[{datetime.now()}] BANNING IP: {ip}")
        subprocess.run(["sudo", "ipset", "add", "blacklist", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        banned_ips[ip] = time.time()

def unban_expired_ips():
    now = time.time()
    for ip in list(banned_ips.keys()):
        if now - banned_ips[ip] > BAN_DURATION:
            print(f"[{datetime.now()}] UNBANNING IP: {ip}")
            subprocess.run(["sudo", "ipset", "del", "blacklist", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            del banned_ips[ip]

def monitor_logs():
    print(">> DoS Defender Mk1 is scanning kernel logs (journalctl -kf)...")
    process = subprocess.Popen(['journalctl', '-kf'], stdout=subprocess.PIPE, text=True)

    while True:
        line = process.stdout.readline()
        if not line:
            break

        match = log_pattern.search(line)
        if match:
            ip = match.group(1)
            ban_ip(ip)

        unban_expired_ips()
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print(">> Stopping DoS Defender Mk1")

