import subprocess
import re
import time
import threading
from collections import defaultdict, deque

# --- Configuration ---
ban_threshold = 5           # Number of SYN FLOOD logs before banning
ban_duration = 3600         # Seconds to ban IP (1 hour)
log_keyword = "SYN FLOOD DROPPED"
check_interval = 0.000001        # Seconds between log line checks

# Track IPs and their timestamps
ip_activity = defaultdict(lambda: deque(maxlen=ban_threshold))
banned_ips = {}

# Regex to extract IPs from log line
ip_regex = re.compile(r'SRC=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)')

# Ban IP with iptables
def ban_ip(ip):
    if ip in banned_ips:
        return
    print(f"[!] Banning IP: {ip}")
    subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    banned_ips[ip] = time.time()

    # Schedule unban
    threading.Thread(target=unban_ip_after_delay, args=(ip,), daemon=True).start()

# Unban IP after delay
def unban_ip_after_delay(ip):
    time.sleep(ban_duration)
    print(f"[+] Unbanning IP: {ip}")
    subprocess.run(["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])
    banned_ips.pop(ip, None)

# Monitor logs
def monitor_logs():
    journal = subprocess.Popen(["journalctl", "-kf"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    for line in iter(journal.stdout.readline, ''):
        if log_keyword not in line:
            continue
        match = ip_regex.search(line)
        if not match:
            continue

        ip = match.group(1)
        now = time.time()
        ip_activity[ip].append(now)

        # If enough hits in short time, ban IP
        if len(ip_activity[ip]) == ban_threshold:
            time_span = ip_activity[ip][-1] - ip_activity[ip][0]
            if time_span <= 60:  # 60 seconds window
                ban_ip(ip)
                ip_activity[ip].clear()

try:
    print("[*] DoS Defender Mk1 is active. Watching logs...")
    monitor_logs()
except KeyboardInterrupt:
    print("\n[!] Stopping DoS Defender Mk1. Goodbye.")
