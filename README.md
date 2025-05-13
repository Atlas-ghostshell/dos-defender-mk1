# dos-defender-mk1
A python-based defensive tool for detecting and mitigating SYN flood DoS attacks using iptables and log monitoring.
# DoS Defender Mk1

**DoS Defender Mk1** is a real-time Python-based firewall enhancement designed to detect and mitigate SYN flood attacks on Linux systems. It actively monitors kernel logs, identifies suspicious patterns, and automatically bans offending IPs using `iptables`, protecting your system from denial-of-service (DoS) attacks.

---

## Project Summary

This project is part of a hands-on cybersecurity defense lab aimed at developing practical skills in DoS mitigation and log-based threat detection. It was built and tested in a virtual lab setup using Kali Linux (attacker) and Ubuntu (target) machines.

---

## Features

- **Real-time log monitoring** using `journalctl`
- **SYN flood detection** based on frequency of dropped packets
- **Automatic IP banning** using `iptables`
- **Timed unbanning** after a cooldown period
- **Customizable thresholds** and log messages

---

## How It Works

1. The system logs dropped SYN packets with a unique prefix using `iptables`.
2. `defender.py` monitors these logs in real time.
3. When a single IP exceeds a specified threshold (e.g. 5 SYN drops per minute), it is:
   - Logged as malicious
   - Automatically banned using an `iptables` rule
4. After a timeout (e.g. 5 minutes), the IP is unbanned automatically.

---

## Setup Instructionsudo python3 defender.py
s

1. **Set iptables rules to drop and log SYN floods:**

bash
sudo iptables -A INPUT -p tcp --syn -m limit --limit 5/minute --limit-burst 5 -j LOG --log-prefix "SYN FLOOD DROPPED: " --log-level 4
sudo iptables -A INPUT -p tcp --syn -j DROP

Run the defender script:
sudo python3 defender.py

(Optional) Make it persistent by running it on boot or as a systemd service.

File Overview

    defender.py: Core detection and response script

    banned_ips.log: Log of all banned IPs with timestamps

    README.md: Documentation for the project

Example Output

DoS Defender Mk1 is active. Watching logs...
[!] Detected repeated SYN flood from 192.168.1.101 - Banning...
[i] 192.168.1.101 successfully banned using iptables
[i] 192.168.1.101 has been unbanned after timeout

Requirements
    Python 3
    Linux (Ubuntu/Debian preferred)
    Access to iptables and journalctl

About the Developer

Geoffrey Muriuki Mwangi
Aspiring SOC Analyst | Cybersecurity Enthusiast | Purple Teamer
LinkedIn: Geoffrey Muriuki
Email: muriukigeoffrey472@gmail.com
Expected Graduation: 2028

Built With Help From
Atlas – AI-powered cybersecurity partner
Co-designed and co-engineered using Atlas for script generation, iptables configuration, and log analysis strategies.

License
MIT License

Final Words
This is just the beginning of a powerful defense system.
Stay sharp, stay curious.
DoS Defender Mk1 was built to defend, but also to learn.
    “We trace the shadows to fortify the light.” — Ghost-shell & PhantomByte Chronicles
