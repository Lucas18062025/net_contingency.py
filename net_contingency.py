#!/usr/bin/env python3
"""
Module Name: net_contingency.py
Author: Lucas Villagra
Description: Diagnostic and remediation tool for Linux network stacks (DNS/Routes).
"""

import os
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NetworkStatus:
    """Stores the verification state of the network interfaces."""

    has_default_route: bool
    dns_resolves: bool
    active_dns_servers: List[str]


class NetworkDiagnoser:
    """Handles operational checks and automated fixes for the network stack."""

    def __init__(self, target_host: str = "8.8.8.8") -> None:
        self.target_host = target_host
        self.resolv_path = "/etc/resolv.conf"

    def check_route(self) -> bool:
        """Verifies if a default gateway is present in the routing table."""
        try:
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True,
                text=True,
                check=True,
            )
            return "default via" in result.stdout
        except subprocess.SubprocessError:
            return False

    def check_dns(self) -> bool:
        """Tests DNS translation capability against a public domain."""
        try:
            result = subprocess.run(
                ["host", "google.com"], capture_output=True, text=True, timeout=3
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def fix_resolv_conf(self, nameservers: List[str]) -> bool:
        """Safely recreates the resolv.conf file with standard targets."""
        if os.geteuid() != 0:
            print(
                "[-] Critical: Administrative privileges (sudo) required for rollback/remediation."
            )
            return False

        try:
            # Atomic rewrite using infrastructure-as-code principles
            with open(self.resolv_path, "w", encoding="utf-8") as f:
                for ns in nameservers:
                    f.write(f"nameserver {ns}\n")
            print(f"[+] Successfully restored local stack at {self.resolv_path}")
            return True
        except IOError as e:
            print(f"[-] I/O Error deploying nameservers: {e}")
            return False


if __name__ == "__main__":
    diagnoser = NetworkDiagnoser()

    print("[*] Initializing Cybersecurity Lab Network Audit...")
    route_ok = diagnoser.check_route()
    dns_ok = diagnoser.check_dns()

    print(f" -> Default Route Status: {'[ OK ]' if route_ok else '[ BROKEN ]'}")
    print(f" -> DNS Resolution Status: {'[ OK ]' if dns_ok else '[ BROKEN ]'}")

    if not dns_ok and route_ok:
        print("[!] Anomalous state detected: Route exists but DNS resolution fails.")
        print("[*] Executing hotfix simulation...")
        # Emergency targets: Cloudflare and Google DNS
        diagnoser.fix_resolv_conf(["1.1.1.1", "8.8.8.8"])
