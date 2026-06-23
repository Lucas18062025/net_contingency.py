#!/usr/bin/env python3
"""
Module Name: net_contingency.py
Author: Lucas Villagra
Description: Production-ready automated network stack diagnostics and DNS remediation tool.
             Supports custom profiles (Google, Cloudflare, Quad9) via argparse.
"""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DNSProfile:
    """Represents a standard secure DNS provider profile."""

    name: str
    servers: List[str]


# Threat Intel & Secure DNS Standard Profiles
DNS_PROVIDERS: Dict[str, DNSProfile] = {
    "google": DNSProfile(name="Google Public DNS", servers=["8.8.8.8", "8.8.4.4"]),
    "cloudflare": DNSProfile(name="Cloudflare DNS", servers=["1.1.1.1", "1.0.0.1"]),
    "quad9": DNSProfile(name="Quad9 Secure DNS", servers=["9.9.9.9", "149.112.112.112"]),
}


class NetworkDiagnoser:
    """Handles network stack state verification and tactical configuration overwrites."""

    def __init__(self, target_host: str = "8.8.8.8") -> None:
        self.target_host = target_host
        self.resolv_path = "/etc/resolv.conf"

    def check_route(self) -> bool:
        """Verifies if a default gateway is active in the routing table."""
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
        """Validates if external name resolution is operational."""
        try:
            result = subprocess.run(
                ["host", "-t", "A", "google.com"],
                capture_output=True,
                text=True,
                timeout=3,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            return False

    def fix_resolv_conf(self, servers: List[str]) -> bool:
        """Safely deploys selected nameservers using atomic I/O operations."""
        if os.geteuid() != 0:
            print(
                "[-] Access Denied: Administrative privileges (sudo) required to modify network configuration."
            )
            return False

        try:
            # Atomic file system writing to avoid partial state corruption
            with open(self.resolv_path, "w", encoding="utf-8") as file:
                file.write("# Generated automatically by Net Contingency tool\n")
                for server in servers:
                    file.write(f"nameserver {server}\n")
            return True
        except IOError as e:
            print(f"[-] Critical I/O Error overwriting configuration matrix: {e}")
            return False


def main() -> None:
    """CLI Entrypoint parsing and lifecycle execution orchestration."""
    parser = argparse.ArgumentParser(
        description="⚙️ Net Contingency: Network diagnostics and automated DNS remediation tool."
    )
    parser.add_argument(
        "-d",
        "--dns",
        choices=list(DNS_PROVIDERS.keys()),
        default="cloudflare",
        help="Select the tactical DNS provider profile to deploy if remediation is needed (default: %(default)s).",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force the injection of selected DNS servers immediately without performing diagnostics.",
    )

    args = parser.parse_args()
    diagnoser = NetworkDiagnoser()

    print("[*] Launching Cybersecurity Lab Network Audit...")

    # Forced deployment branch
    if args.force:
        profile = DNS_PROVIDERS[args.dns]
        print(f"[!] Force flag detected. Deploying [{profile.name}] profiles...")
        if diagnoser.fix_resolv_conf(profile.servers):
            print("[+] Target infrastructure updated successfully.")
        sys.exit(0)

    # Diagnostic flow branch
    route_status = diagnoser.check_route()
    dns_status = diagnoser.check_dns()

    print(f" -> Default Gateway State: {'[ OK ]' if route_status else '[ DISCONNECTED ]'}")
    print(f" -> Name Resolution State: {'[ OK ]' if dns_status else '[ FAILED ]'}")

    if not route_status:
        print("[-] Critical Error: Physical interface down or missing default gateway route.")
        sys.exit(1)

    if not dns_status:
        profile = DNS_PROVIDERS[args.dns]
        print(f"[🚨] DNS Failure detected! Deploying tactical hotfix with profile: [{profile.name}]")
        if diagnoser.fix_resolv_conf(profile.servers):
            print("[+] Remediation successfully applied. Re-testing stack resolution...")
            if diagnoser.check_dns():
                print("[✅] Network operation restored to regular parameters.")
            else:
                print("[-] Warning: Configuration updated but DNS queries remain filtered.")
    else:
        print("[✅] System stable. No tactical mitigation actions required.")


if __name__ == "__main__":
    main()
