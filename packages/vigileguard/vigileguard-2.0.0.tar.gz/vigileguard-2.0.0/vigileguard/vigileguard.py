#!/usr/bin/env python3
"""
VigileGuard - Linux Security Audit Tool (Phase 1)
A comprehensive security audit tool for Linux systems

Repository: https://github.com/navinnm/VigileGuard
Author: VigileGuard Development Team
License: MIT
Version: 1.0.5
"""

import os
import sys
import json
import yaml
import subprocess
import stat
import pwd
import grp
import platform
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Add current directory to Python path to help with imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import rich components with error handling
RICH_AVAILABLE = True
try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError as e:
    RICH_AVAILABLE = False
    print(f"Warning: Rich library not available ({e}). Using fallback mode.")
    # Define minimal fallback classes
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    
    class Panel:
        @staticmethod
        def fit(text, **kwargs):
            return text

__version__ = "1.0.5"

# Global console for rich output
console = Console()


class SeverityLevel(Enum):
    """Security finding severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class Finding:
    """Represents a security finding"""
    category: str
    severity: SeverityLevel
    title: str
    description: str
    recommendation: str
    details: Optional[Dict[str, Any]] = None  

    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary"""
        result = asdict(self)
        result["severity"] = self.severity.value
        return result


class SecurityChecker:
    """Base class for all security checkers"""

    def __init__(self):
        self.findings: List[Finding] = []

    def check(self) -> List[Finding]:
        """Run the security check - to be implemented by subclasses"""
        raise NotImplementedError

    def add_finding(self, category: str, severity: SeverityLevel, title: str,
                description: str, recommendation: str, 
                details: Optional[Dict[str, Any]] = None):
        """Add a security finding"""
        finding = Finding(
            category=category,
            severity=severity,
            title=title,
            description=description,
            recommendation=recommendation,
            details=details or {}
        )
        self.findings.append(finding)

    def run_command(self, command: str) -> tuple:
        """Execute a shell command and return output"""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)


class FilePermissionChecker(SecurityChecker):
    """Check file and directory permissions for security issues"""

    def check(self) -> List[Finding]:
        """Run file permission checks"""
        if RICH_AVAILABLE:
            console.print("🔍 Checking file permissions...", style="yellow")
        else:
            print("🔍 Checking file permissions...")

        # Check world-writable files
        self._check_world_writable_files()

        # Check SUID/SGID binaries
        self._check_suid_sgid_files()

        # Check sensitive file permissions
        self._check_sensitive_files()

        # Check home directory permissions
        self._check_home_directories()

        return self.findings

    def _check_world_writable_files(self):
        """Find world-writable files and directories"""
        cmd = "find /etc /usr /var -type f -perm -002 2>/dev/null | head -20"
        returncode, stdout, stderr = self.run_command(cmd)

        if returncode == 0 and stdout.strip():
            files = [f for f in stdout.strip().split('\n') if f]
            if files:
                self.add_finding(
                    category="File Permissions",
                    severity=SeverityLevel.HIGH,
                    title="World-writable files found",
                    description=(f"Found {len(files)} world-writable files "
                                f"in system directories"),
                    recommendation="Remove world-write permissions: chmod o-w <filename>",
                    details={"files": files[:10]}  # Limit to first 10
                )

    def _check_suid_sgid_files(self):
        """Find SUID and SGID binaries"""
        cmd = ("find /usr /bin /sbin -type f \\( -perm -4000 -o -perm -2000 \\) "
               "2>/dev/null")
        returncode, stdout, stderr = self.run_command(cmd)

        if returncode == 0 and stdout.strip():
            files = stdout.strip().split('\n')

            # Known safe SUID/SGID files (common ones)
            safe_files = {
                '/usr/bin/sudo', '/usr/bin/su', '/usr/bin/passwd',
                '/usr/bin/chsh', '/usr/bin/chfn', '/usr/bin/newgrp',
                '/usr/bin/gpasswd', '/bin/ping', '/bin/mount', '/bin/umount'
            }

            suspicious_files = [f for f in files if f not in safe_files]

            if suspicious_files:
                self.add_finding(
                    category="File Permissions",
                    severity=SeverityLevel.MEDIUM,
                    title="Unusual SUID/SGID binaries found",
                    description=(f"Found {len(suspicious_files)} potentially "
                                f"unnecessary SUID/SGID files"),
                    recommendation=("Review each file and remove SUID/SGID bits if not "
                                   "needed: chmod u-s <filename>"),
                    details={"files": suspicious_files}
                )

    def _check_sensitive_files(self):
        """Check permissions on sensitive system files"""
        sensitive_files = {
            '/etc/passwd': (0o644, 'root', 'root'),
            '/etc/shadow': (0o640, 'root', 'shadow'),
            '/etc/group': (0o644, 'root', 'root'),
            '/etc/gshadow': (0o640, 'root', 'shadow'),
            '/etc/sudoers': (0o440, 'root', 'root'),
        }

        for filepath, (expected_mode, expected_owner, expected_group) in sensitive_files.items():
            if os.path.exists(filepath):
                try:
                    stat_info = os.stat(filepath)
                    actual_mode = stat.S_IMODE(stat_info.st_mode)
                    actual_owner = pwd.getpwuid(stat_info.st_uid).pw_name
                    actual_group = grp.getgrgid(stat_info.st_gid).gr_name

                    issues = []
                    if actual_mode != expected_mode:
                        issues.append(f"mode {oct(actual_mode)} "
                                     f"(expected {oct(expected_mode)})")
                    if actual_owner != expected_owner:
                        issues.append(f"owner {actual_owner} "
                                     f"(expected {expected_owner})")
                    if actual_group != expected_group:
                        issues.append(f"group {actual_group} "
                                     f"(expected {expected_group})")

                    if issues:
                        self.add_finding(
                            category="File Permissions",
                            severity=SeverityLevel.HIGH,
                            title=f"Incorrect permissions on {filepath}",
                            description=(f"Security-sensitive file has incorrect "
                                        f"{', '.join(issues)}"),
                            recommendation=(f"Fix with: chown {expected_owner}:"
                                          f"{expected_group} {filepath} && "
                                          f"chmod {oct(expected_mode)} {filepath}"),
                            details={"file": filepath, "issues": issues}
                        )
                except (OSError, KeyError):
                    pass

    def _check_home_directories(self):
        """Check home directory permissions"""
        cmd = "find /home -maxdepth 1 -type d -perm -002 2>/dev/null"
        returncode, stdout, stderr = self.run_command(cmd)

        if returncode == 0 and stdout.strip():
            dirs = [d for d in stdout.strip().split('\n')
                   if d and d != '/home']
            if dirs:
                self.add_finding(
                    category="File Permissions",
                    severity=SeverityLevel.MEDIUM,
                    title="World-writable home directories found",
                    description=f"Found {len(dirs)} world-writable home directories",
                    recommendation="Remove world-write permissions: chmod o-w <directory>",
                    details={"directories": dirs}
                )

class UserAccountChecker(SecurityChecker):
    """Check user accounts and authentication settings"""
    
    def check(self) -> List[Finding]:
        """Run user account security checks"""
        if RICH_AVAILABLE:
            console.print("👥 Checking user accounts...", style="yellow")
        else:
            print("👥 Checking user accounts...")
        
        # Check for accounts with empty passwords
        self._check_empty_passwords()
        
        # Check for duplicate UIDs
        self._check_duplicate_uids()
        
        # Check sudo configuration
        self._check_sudo_config()
        
        # Check password policies
        self._check_password_policies()
        
        return self.findings
    
    def _check_empty_passwords(self):
        """Check for accounts with empty passwords"""
        try:
            with open('/etc/shadow', 'r') as f:
                lines = f.readlines()
            
            empty_password_accounts = []
            for line in lines:
                if line.strip():
                    parts = line.split(':')
                    if len(parts) >= 2 and parts[1] == '':
                        empty_password_accounts.append(parts[0])
            
            if empty_password_accounts:
                self.add_finding(
                    category="User Accounts",
                    severity=SeverityLevel.CRITICAL,
                    title="Accounts with empty passwords found",
                    description=f"Found {len(empty_password_accounts)} accounts with empty passwords",
                    recommendation="Set passwords for all accounts or disable them: passwd <username> or usermod -L <username>",
                    details={"accounts": empty_password_accounts}
                )
        except (OSError, PermissionError):
            self.add_finding(
                category="User Accounts",
                severity=SeverityLevel.INFO,
                title="Cannot read /etc/shadow",
                description="Insufficient permissions to check for empty passwords",
                recommendation="Run VigileGuard with appropriate privileges"
            )
    
    def _check_duplicate_uids(self):
        """Check for duplicate UIDs"""
        uid_map = {}
        try:
            with open('/etc/passwd', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) >= 3:
                            username = parts[0]
                            uid = parts[2]
                            
                            if uid in uid_map:
                                uid_map[uid].append(username)
                            else:
                                uid_map[uid] = [username]
            
            duplicates = {uid: users for uid, users in uid_map.items() if len(users) > 1}
            
            if duplicates:
                self.add_finding(
                    category="User Accounts",
                    severity=SeverityLevel.HIGH,
                    title="Duplicate UIDs found",
                    description=f"Found {len(duplicates)} UIDs assigned to multiple users",
                    recommendation="Assign unique UIDs to each user account",
                    details={"duplicates": duplicates}
                )
        except OSError:
            pass

    def _check_sudo_config(self):
        """Check sudo configuration"""
        if os.path.exists('/etc/sudoers'):
            cmd = "sudo -l 2>/dev/null || echo 'Cannot check sudo'"
            returncode, stdout, stderr = self.run_command(cmd)
            
            # Check for dangerous sudo configurations
            try:
                # This requires appropriate permissions
                cmd = "grep -E '(NOPASSWD:ALL|%.*ALL.*NOPASSWD)' /etc/sudoers /etc/sudoers.d/* 2>/dev/null || true"
                returncode, stdout, stderr = self.run_command(cmd)
                
                if stdout.strip():
                    self.add_finding(
                        category="User Accounts",
                        severity=SeverityLevel.HIGH,
                        title="Permissive sudo configuration found",
                        description="Found sudo rules that allow passwordless execution of all commands",
                        recommendation="Review sudo configuration and require passwords for sensitive operations",
                        details={"matches": stdout.strip().split('\n')}
                    )
            except:
                pass
    
    def _check_password_policies(self):
        """Check password policy configuration"""
        # Check if PAM password quality is configured
        pam_files = ['/etc/pam.d/common-password', '/etc/pam.d/system-auth']
        
        pam_configured = False
        for pam_file in pam_files:
            if os.path.exists(pam_file):
                try:
                    with open(pam_file, 'r') as f:
                        content = f.read()
                        if 'pam_pwquality' in content or 'pam_cracklib' in content:
                            pam_configured = True
                            break
                except OSError:
                    pass
        
        if not pam_configured:
            self.add_finding(
                category="User Accounts",
                severity=SeverityLevel.MEDIUM,
                title="No password quality checking configured",
                description="PAM password quality modules not found",
                recommendation="Configure pam_pwquality or pam_cracklib for password strength checking",
                details={}
            )

class SSHConfigChecker(SecurityChecker):
    """Check SSH configuration for security issues"""
    
    def check(self) -> List[Finding]:
        """Run SSH configuration checks"""
        if RICH_AVAILABLE:
            console.print("🔑 Checking SSH configuration...", style="yellow")
        else:
            print("🔑 Checking SSH configuration...")
        
        if not os.path.exists('/etc/ssh/sshd_config'):
            self.add_finding(
                category="SSH",
                severity=SeverityLevel.INFO,
                title="SSH server not installed",
                description="SSH server configuration not found",
                recommendation="Install and configure SSH server if remote access is needed"
            )
            return self.findings
        
        self._check_ssh_config()
        self._check_ssh_keys()
        
        return self.findings
    
    def _check_ssh_config(self):
        """Analyze SSH configuration file"""
        try:
            with open('/etc/ssh/sshd_config', 'r') as f:
                config_lines = f.readlines()
        except OSError:
            return
        
        config = {}
        for line in config_lines:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(None, 1)
                if len(parts) == 2:
                    config[parts[0].lower()] = parts[1]
        
        # Security checks
        security_settings = {
            'permitrootlogin': ('no', SeverityLevel.HIGH, 
                              "Root login should be disabled",
                              "Set 'PermitRootLogin no' in /etc/ssh/sshd_config"),
            'passwordauthentication': ('no', SeverityLevel.MEDIUM,
                                     "Password authentication should be disabled",
                                     "Set 'PasswordAuthentication no' and use key-based authentication"),
            'permitemptypasswords': ('no', SeverityLevel.CRITICAL,
                                   "Empty passwords should not be permitted",
                                   "Set 'PermitEmptyPasswords no' in /etc/ssh/sshd_config"),
            'protocol': ('2', SeverityLevel.HIGH,
                        "Only SSH protocol version 2 should be used",
                        "Set 'Protocol 2' in /etc/ssh/sshd_config"),
        }
        
        for setting, (expected_value, severity, description, recommendation) in security_settings.items():
            actual_value = config.get(setting, 'default')
            
            # Handle default values
            if setting == 'permitrootlogin' and actual_value == 'default':
                actual_value = 'yes'  # Default is usually yes
            elif setting == 'passwordauthentication' and actual_value == 'default':
                actual_value = 'yes'  # Default is usually yes
            elif setting == 'permitemptypasswords' and actual_value == 'default':
                actual_value = 'no'   # Default is usually no
            
            if actual_value.lower() != expected_value.lower():
                self.add_finding(
                    category="SSH",
                    severity=severity,
                    title=f"Insecure SSH setting: {setting}",
                    description=f"{description}. Current: {actual_value}",
                    recommendation=recommendation,
                    details={"setting": setting, "current": actual_value, "recommended": expected_value}
                )
        
        # Check for specific port configuration
        port = config.get('port', '22')
        if port == '22':
            self.add_finding(
                category="SSH",
                severity=SeverityLevel.LOW,
                title="SSH running on default port",
                description="SSH is running on the default port 22",
                recommendation="Consider changing SSH port to a non-standard port for security through obscurity",
                details={"current_port": port}
            )
    
    def _check_ssh_keys(self):
        """Check SSH host keys and user keys"""
        # Check host key permissions
        host_key_files = [
            '/etc/ssh/ssh_host_rsa_key',
            '/etc/ssh/ssh_host_ecdsa_key',
            '/etc/ssh/ssh_host_ed25519_key'
        ]
        
        for key_file in host_key_files:
            if os.path.exists(key_file):
                try:
                    stat_info = os.stat(key_file)
                    mode = stat.S_IMODE(stat_info.st_mode)
                    
                    if mode != 0o600:
                        self.add_finding(
                            category="SSH",
                            severity=SeverityLevel.HIGH,
                            title=f"Incorrect permissions on SSH host key",
                            description=f"SSH host key {key_file} has permissions {oct(mode)} (should be 600)",
                            recommendation=f"Fix permissions: chmod 600 {key_file}",
                            details={"file": key_file, "current_mode": oct(mode)}
                        )
                except OSError:
                    pass

class SystemInfoChecker(SecurityChecker):
    """Gather basic system information and check for security-relevant details"""
    
    def check(self) -> List[Finding]:
        """Run system information checks"""
        if RICH_AVAILABLE:
            console.print("💻 Gathering system information...", style="yellow")
        else:
            print("💻 Gathering system information...")
        
        self._check_os_version()
        self._check_kernel_version()
        self._check_running_services()
        
        return self.findings
    
    def _check_os_version(self):
        """Check OS version and support status"""
        try:
            # Get OS release information
            os_info = {}
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            os_info[key] = value.strip('"')
            
            os_name = os_info.get('NAME', 'Unknown')
            os_version = os_info.get('VERSION', 'Unknown')
            
            self.add_finding(
                category="System Info",
                severity=SeverityLevel.INFO,
                title="Operating System Information",
                description=f"Running {os_name} {os_version}",
                recommendation="Ensure OS is supported and receiving security updates",
                details={"os_info": os_info}
            )
            
            # Check for end-of-life versions (simplified check)
            if 'ubuntu' in os_name.lower():
                version_num = os_info.get('VERSION_ID', '')
                if version_num in ['14.04', '16.04']:  # Example EOL versions
                    self.add_finding(
                        category="System Info",
                        severity=SeverityLevel.HIGH,
                        title="End-of-life operating system",
                        description=f"Ubuntu {version_num} is no longer supported",
                        recommendation="Upgrade to a supported Ubuntu version",
                        details={"version": version_num}
                    )
                    
        except OSError:
            pass
    
    def _check_kernel_version(self):
        """Check kernel version"""
        kernel_version = platform.release()
        
        self.add_finding(
            category="System Info",
            severity=SeverityLevel.INFO,
            title="Kernel Information",
            description=f"Running kernel version {kernel_version}",
            recommendation="Keep kernel updated to latest version for security patches",
            details={"kernel_version": kernel_version}
        )
    
    def _check_running_services(self):
        """Check for potentially risky running services"""
        risky_services = {
            'telnet': SeverityLevel.CRITICAL,
            'rsh': SeverityLevel.CRITICAL,
            'ftp': SeverityLevel.HIGH,
            'tftp': SeverityLevel.HIGH,
            'finger': SeverityLevel.MEDIUM,
            'rlogin': SeverityLevel.CRITICAL
        }
        
        # Check systemd services
        cmd = "systemctl list-units --type=service --state=active --no-pager --no-legend 2>/dev/null || true"
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode == 0 and stdout:
            active_services = []
            for line in stdout.split('\n'):
                if line.strip():
                    service_name = line.split()[0].replace('.service', '')
                    active_services.append(service_name)
            
            found_risky = []
            for service in active_services:
                for risky_service, severity in risky_services.items():
                    if risky_service in service.lower():
                        found_risky.append((service, severity))
            
            if found_risky:
                for service, severity in found_risky:
                    self.add_finding(
                        category="System Info",
                        severity=severity,
                        title=f"Risky service running: {service}",
                        description=f"Potentially insecure service '{service}' is active",
                        recommendation=f"Consider disabling {service} if not needed: systemctl disable {service}",
                        details={"service": service}
                    )

class AuditEngine:
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.checkers = [
            FilePermissionChecker(),
            UserAccountChecker(), 
            SSHConfigChecker(),
            SystemInfoChecker()
        ]
        self.all_findings: List[Finding] = []
        
        # Try to add Phase 2 checkers if available
        self.phase2_available = False
        try:
            # Import Phase 2 checkers with multiple fallback methods
            web_checkers = None
            try:
                # Try relative import first
                from .web_security_checkers import WebServerSecurityChecker, NetworkSecurityChecker
                web_checkers = (WebServerSecurityChecker, NetworkSecurityChecker)
            except ImportError:
                try:
                    # Try absolute import
                    from web_security_checkers import WebServerSecurityChecker, NetworkSecurityChecker
                    web_checkers = (WebServerSecurityChecker, NetworkSecurityChecker)
                except ImportError:
                    # Try importing from current directory
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(
                        "web_security_checkers", 
                        os.path.join(current_dir, "web_security_checkers.py")
                    )
                    if spec and spec.loader:
                        web_mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(web_mod)
                        web_checkers = (web_mod.WebServerSecurityChecker, web_mod.NetworkSecurityChecker)
            
            if web_checkers:
                self.checkers.extend([
                    web_checkers[0](),
                    web_checkers[1]()
                ])
                if RICH_AVAILABLE:
                    console.print("✅ Phase 2 components loaded successfully", style="green")
                else:
                    print("✅ Phase 2 components loaded successfully")
                self.phase2_available = True
            
        except ImportError as e:
            if RICH_AVAILABLE:
                console.print(f"⚠️ Phase 2 components not available: {e}", style="yellow")
            else:
                print(f"⚠️ Phase 2 components not available: {e}")

    def _get_scan_info(self) -> Dict[str, Any]:
        """Get scan information dictionary"""
        return {
            'timestamp': datetime.now().isoformat(),
            'tool': 'VigileGuard',
            'version': '2.0.0' if self.phase2_available else __version__,
            'hostname': platform.node(),
            'repository': 'https://github.com/navinnm/VigileGuard'
        }
        
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "output_format": "console",
            "severity_filter": "INFO",
            "excluded_checks": [],
            "custom_rules": {}
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                        custom_config = yaml.safe_load(f)
                    else:
                        custom_config = json.load(f)
                if custom_config is not None:  # Check for None first
                    default_config.update(custom_config)
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"Warning: Could not load config file: {e}", style="yellow")
                else:
                    print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def run_audit(self) -> List[Finding]:
        """Run all security checks"""
        if RICH_AVAILABLE:
            console.print(Panel.fit("🛡️ VigileGuard Security Audit", style="bold blue"))
            console.print(f"Starting audit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            console.print()
        else:
            print("🛡️ VigileGuard Security Audit")
            print(f"Starting audit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                
                for checker in self.checkers:
                    task = progress.add_task(f"Running {checker.__class__.__name__}...", total=None)
                    try:
                        findings = checker.check()
                        self.all_findings.extend(findings)
                        progress.update(task, completed=True)
                    except Exception as e:
                        console.print(f"Error in {checker.__class__.__name__}: {e}", style="red")
                        progress.update(task, completed=True)
        else:
            # Fallback without rich
            for checker in self.checkers:
                print(f"Running {checker.__class__.__name__}...")
                try:
                    findings = checker.check()
                    self.all_findings.extend(findings)
                    print(f"✅ {checker.__class__.__name__} completed")
                except Exception as e:
                    print(f"❌ Error in {checker.__class__.__name__}: {e}")
        
        return self.all_findings
    
    def generate_report(self, format_type: str = "console") -> str:
        """Generate report in specified format"""
        if format_type == "console":
            return self._generate_console_report()
        elif format_type == "json":
            return self._generate_json_report()
        elif format_type == "html":
            # Try to use Phase 2 HTML reporter if available
            try:
                # Try multiple import methods for enhanced_reporting
                enhanced_reporting = None
                try:
                    from .enhanced_reporting import HTMLReporter
                    enhanced_reporting = HTMLReporter
                except ImportError:
                    try:
                        from enhanced_reporting import HTMLReporter
                        enhanced_reporting = HTMLReporter
                    except ImportError:
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(
                            "enhanced_reporting", 
                            os.path.join(current_dir, "enhanced_reporting.py")
                        )
                        if spec and spec.loader:
                            enhanced_mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(enhanced_mod)
                            enhanced_reporting = enhanced_mod.HTMLReporter
                
                if enhanced_reporting:
                    html_reporter = enhanced_reporting(self.all_findings, self._get_scan_info())
                    return html_reporter.generate_report("report.html")
            except ImportError:
                if RICH_AVAILABLE:
                    console.print("❌ HTML format requires Phase 2 components", style="red")
                else:
                    print("❌ HTML format requires Phase 2 components")
                return ""
        else:
            return self._generate_console_report()
    
    def _generate_console_report(self) -> str:
        """Generate console-friendly report"""
        if RICH_AVAILABLE:
            console.print()
            console.print(Panel.fit("📊 Audit Results", style="bold green"))
        else:
            print("\n📊 Audit Results")
        
        # Count findings by severity
        severity_counts = {level: 0 for level in SeverityLevel}
        for finding in self.all_findings:
            severity_counts[finding.severity] += 1
        
        if RICH_AVAILABLE:
            # Summary table
            summary_table = Table(title="Summary")
            summary_table.add_column("Severity", style="bold")
            summary_table.add_column("Count", justify="right")
            
            severity_colors = {
                SeverityLevel.CRITICAL: "red",
                SeverityLevel.HIGH: "orange1", 
                SeverityLevel.MEDIUM: "yellow",
                SeverityLevel.LOW: "blue",
                SeverityLevel.INFO: "green"
            }
            
            for severity, count in severity_counts.items():
                if count > 0:
                    color = severity_colors.get(severity, "white")
                    summary_table.add_row(severity.value, str(count), style=color)
            
            console.print(summary_table)
            console.print()
        else:
            # Fallback without rich
            print("\nSummary:")
            for severity, count in severity_counts.items():
                if count > 0:
                    print(f"  {severity.value}: {count}")
        
        # Detailed findings
        if self.all_findings:
            if RICH_AVAILABLE:
                severity_colors = {
                    SeverityLevel.CRITICAL: "red",
                    SeverityLevel.HIGH: "orange1", 
                    SeverityLevel.MEDIUM: "yellow",
                    SeverityLevel.LOW: "blue",
                    SeverityLevel.INFO: "green"
                }
                for finding in sorted(self.all_findings, key=lambda x: list(SeverityLevel).index(x.severity)):
                    color = severity_colors.get(finding.severity, "white")
                    
                    finding_panel = Panel(
                        f"[bold]{finding.title}[/bold]\n\n"
                        f"[italic]{finding.description}[/italic]\n\n"
                        f"💡 [bold]Recommendation:[/bold] {finding.recommendation}",
                        title=f"[{color}]{finding.severity.value}[/{color}] - {finding.category}",
                        border_style=color
                    )
                    console.print(finding_panel)
                    console.print()
            else:
                # Fallback without rich
                for finding in sorted(self.all_findings, key=lambda x: list(SeverityLevel).index(x.severity)):
                    print(f"\n[{finding.severity.value}] {finding.category}: {finding.title}")
                    print(f"Description: {finding.description}")
                    print(f"Recommendation: {finding.recommendation}")
        else:
            if RICH_AVAILABLE:
                console.print("✅ No security issues found!", style="bold green")
            else:
                print("✅ No security issues found!")
        
        return ""
    
    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        report = {
            "scan_info": self._get_scan_info(),
            "summary": {
                "total_findings": len(self.all_findings),
                "by_severity": {}
            },
            "findings": [finding.to_dict() for finding in self.all_findings]
        }
        
        # Count by severity
        for finding in self.all_findings:
            severity = finding.severity.value
            report["summary"]["by_severity"][severity] = report["summary"]["by_severity"].get(severity, 0) + 1
        
        return json.dumps(report, indent=2)

@click.command()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', 'output_format', default='console', 
              type=click.Choice(['console', 'json', 'html', 'compliance', 'all']), 
              help='Output format')
@click.option('--environment', '-e', help='Environment (development/staging/production)')
@click.option('--notifications', is_flag=True, help='Enable notifications')
@click.option('--debug', is_flag=True, help='Enable debug output')
@click.version_option(version=__version__)
def main(config: Optional[str], output: Optional[str], output_format: str, 
         environment: Optional[str], notifications: bool, debug: bool):
    """
    VigileGuard - Linux Security Audit Tool
    
    Performs comprehensive security audits including:
    - File permission analysis
    - User account security checks  
    - SSH configuration review
    - System information gathering
    - Web server security (if Phase 2 available)
    - Network security analysis (if Phase 2 available)
    
    Repository: https://github.com/navinnm/VigileGuard
    """
    try:
        # Check if Phase 2 components are available
        phase2_available = False
        try:
            # Try multiple import methods for Phase 2 components
            phase2_integration = None
            try:
                from .phase2_integration import Phase2AuditEngine
                from .enhanced_reporting import ReportManager, HTMLReporter, ComplianceMapper
                phase2_integration = Phase2AuditEngine
                phase2_available = True
            except ImportError:
                try:
                    from phase2_integration import Phase2AuditEngine
                    from enhanced_reporting import ReportManager, HTMLReporter, ComplianceMapper
                    phase2_integration = Phase2AuditEngine
                    phase2_available = True
                except ImportError:
                    # Try importing from current directory
                    import importlib.util
                    phase2_spec = importlib.util.spec_from_file_location(
                        "phase2_integration", 
                        os.path.join(current_dir, "phase2_integration.py")
                    )
                    if phase2_spec and phase2_spec.loader:
                        phase2_mod = importlib.util.module_from_spec(phase2_spec)
                        phase2_spec.loader.exec_module(phase2_mod)
                        phase2_integration = phase2_mod.Phase2AuditEngine
                        phase2_available = True
            
            if phase2_available:
                if RICH_AVAILABLE:
                    console.print("✅ Phase 2 features available", style="green")
                else:
                    print("✅ Phase 2 features available")
        except ImportError as e:
            if output_format in ['html', 'compliance', 'all']:
                if RICH_AVAILABLE:
                    console.print(f"❌ Phase 2 features required for {output_format} format", style="red")
                    console.print("Please ensure Phase 2 files are in the same directory:", style="yellow")
                    console.print("  - web_security_checkers.py", style="yellow")
                    console.print("  - enhanced_reporting.py", style="yellow") 
                    console.print("  - phase2_integration.py", style="yellow")
                else:
                    print(f"❌ Phase 2 features required for {output_format} format")
                    print("Please ensure Phase 2 files are in the same directory:")
                    print("  - web_security_checkers.py")
                    print("  - enhanced_reporting.py") 
                    print("  - phase2_integration.py")
                sys.exit(1)
            phase2_available = False
            if RICH_AVAILABLE:
                console.print(f"⚠️ Phase 2 components not available: {e}", style="yellow")
            else:
                print(f"⚠️ Phase 2 components not available: {e}")
        
        # Initialize appropriate engine based on available features
        if phase2_available and phase2_integration:
            # Use Phase 2 enhanced engine
            engine = phase2_integration(config, environment)
        else:
            # Use original Phase 1 engine
            engine = AuditEngine(config)
        
        # Run the audit
        findings = engine.run_audit()
        
        # Generate reports based on format
        scan_info = {
            'timestamp': datetime.now().isoformat(),
            'tool': 'VigileGuard',
            'version': '2.0.0' if phase2_available else __version__,
            'hostname': platform.node(),
            'repository': 'https://github.com/navinnm/VigileGuard'
        }
        
        if output_format == 'console' and not output:
            # Console output is handled by the engine
            pass
        elif output_format == 'json':
            # JSON output
            if phase2_available:
                try:
                    # Try to import ReportManager
                    report_manager = None
                    try:
                        from .enhanced_reporting import ReportManager
                        report_manager = ReportManager
                    except ImportError:
                        try:
                            from enhanced_reporting import ReportManager
                            report_manager = ReportManager
                        except ImportError:
                            import importlib.util
                            spec = importlib.util.spec_from_file_location(
                                "enhanced_reporting", 
                                os.path.join(current_dir, "enhanced_reporting.py")
                            )
                            if spec and spec.loader:
                                enhanced_mod = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(enhanced_mod)
                                report_manager = enhanced_mod.ReportManager
                    
                    if report_manager:
                        rm = report_manager(findings, scan_info)
                        report_content = rm.generate_technical_report()
                    else:
                        report_content = engine.generate_report('json')
                except ImportError:
                    # Fall back to Phase 1 JSON generation
                    report_content = engine.generate_report('json')
            else:
                # Use original JSON generation
                report_content = engine.generate_report('json')
            
            if output:
                with open(output, 'w') as f:
                    if isinstance(report_content, str):
                        f.write(report_content)
                    else:
                        json.dump(report_content, f, indent=2, default=str)
                if RICH_AVAILABLE:
                    console.print(f"JSON report saved to {output}", style="green")
                else:
                    print(f"JSON report saved to {output}")
            else:
                if isinstance(report_content, str):
                    print(report_content)
                else:
                    print(json.dumps(report_content, indent=2, default=str))
        
        elif output_format == 'html':
            if not phase2_available:
                if RICH_AVAILABLE:
                    console.print("❌ HTML format requires Phase 2 components", style="red")
                else:
                    print("❌ HTML format requires Phase 2 components")
                sys.exit(1)
            
            # HTML output (Phase 2)
            try:
                # Try to import HTMLReporter
                html_reporter = None
                try:
                    from .enhanced_reporting import HTMLReporter
                    html_reporter = HTMLReporter
                except ImportError:
                    try:
                        from enhanced_reporting import HTMLReporter
                        html_reporter = HTMLReporter
                    except ImportError:
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(
                            "enhanced_reporting", 
                            os.path.join(current_dir, "enhanced_reporting.py")
                        )
                        if spec and spec.loader:
                            enhanced_mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(enhanced_mod)
                            html_reporter = enhanced_mod.HTMLReporter
                
                if html_reporter:
                    reporter = html_reporter(findings, scan_info)
                    output_file = output or f"vigileguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                    reporter.generate_report(output_file)
                    if RICH_AVAILABLE:
                        console.print(f"HTML report saved to {output_file}", style="green")
                    else:
                        print(f"HTML report saved to {output_file}")
                else:
                    raise ImportError("HTMLReporter not available")
            except ImportError:
                if RICH_AVAILABLE:
                    console.print("❌ HTML format requires Phase 2 components", style="red")
                else:
                    print("❌ HTML format requires Phase 2 components")
                sys.exit(1)
        
        elif output_format == 'compliance':
            if not phase2_available:
                if RICH_AVAILABLE:
                    console.print("❌ Compliance format requires Phase 2 components", style="red")
                else:
                    print("❌ Compliance format requires Phase 2 components")
                sys.exit(1)
            
            # Compliance output (Phase 2)
            try:
                # Try to import ComplianceMapper
                compliance_mapper = None
                try:
                    from .enhanced_reporting import ComplianceMapper
                    compliance_mapper = ComplianceMapper
                except ImportError:
                    try:
                        from enhanced_reporting import ComplianceMapper
                        compliance_mapper = ComplianceMapper
                    except ImportError:
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(
                            "enhanced_reporting", 
                            os.path.join(current_dir, "enhanced_reporting.py")
                        )
                        if spec and spec.loader:
                            enhanced_mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(enhanced_mod)
                            compliance_mapper = enhanced_mod.ComplianceMapper
                
                if compliance_mapper:
                    mapper = compliance_mapper()
                    compliance_report = mapper.generate_compliance_report(findings)
                    output_file = output or f"vigileguard_compliance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    
                    with open(output_file, 'w') as f:
                        json.dump(compliance_report, f, indent=2, default=str)
                    if RICH_AVAILABLE:
                        console.print(f"Compliance report saved to {output_file}", style="green")
                    else:
                        print(f"Compliance report saved to {output_file}")
                else:
                    raise ImportError("ComplianceMapper not available")
            except ImportError:
                if RICH_AVAILABLE:
                    console.print("❌ Compliance format requires Phase 2 components", style="red")
                else:
                    print("❌ Compliance format requires Phase 2 components")
                sys.exit(1)
        
        elif output_format == 'all':
            if not phase2_available:
                if RICH_AVAILABLE:
                    console.print("❌ 'all' format requires Phase 2 components", style="red")
                else:
                    print("❌ 'all' format requires Phase 2 components")
                sys.exit(1)
            
            # Generate all formats (Phase 2)
            try:
                # Try to import ReportManager
                report_manager = None
                try:
                    from .enhanced_reporting import ReportManager
                    report_manager = ReportManager
                except ImportError:
                    try:
                        from enhanced_reporting import ReportManager
                        report_manager = ReportManager
                    except ImportError:
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(
                            "enhanced_reporting", 
                            os.path.join(current_dir, "enhanced_reporting.py")
                        )
                        if spec and spec.loader:
                            enhanced_mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(enhanced_mod)
                            report_manager = enhanced_mod.ReportManager
                
                if report_manager:
                    rm = report_manager(findings, scan_info)
                    output_dir = output or './reports'
                    generated_files = rm.generate_all_formats(output_dir)
                    
                    if RICH_AVAILABLE:
                        console.print("📊 All reports generated:", style="bold green")
                        for format_type, file_path in generated_files.items():
                            console.print(f"  {format_type.upper()}: {file_path}")
                    else:
                        print("📊 All reports generated:")
                        for format_type, file_path in generated_files.items():
                            print(f"  {format_type.upper()}: {file_path}")
                else:
                    raise ImportError("ReportManager not available")
            except ImportError:
                if RICH_AVAILABLE:
                    console.print("❌ 'all' format requires Phase 2 components", style="red")
                else:
                    print("❌ 'all' format requires Phase 2 components")
                sys.exit(1)
        
        # Send notifications if enabled (Phase 2)
        if notifications and phase2_available:
            try:
                if hasattr(engine, 'notification_manager'):
                    engine.notification_manager.send_notifications(findings, scan_info)
                    if RICH_AVAILABLE:
                        console.print("📧 Notifications sent", style="green")
                    else:
                        print("📧 Notifications sent")
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"⚠️ Notification failed: {e}", style="yellow")
                else:
                    print(f"⚠️ Notification failed: {e}")
        
        # Exit with appropriate code
        critical_high_count = sum(1 for f in findings 
                                if f.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH])
        
        if critical_high_count > 0:
            if RICH_AVAILABLE:
                console.print(f"\n⚠️  Found {critical_high_count} critical/high severity issues", style="red")
            else:
                print(f"\n⚠️  Found {critical_high_count} critical/high severity issues")
            sys.exit(1)
        else:
            if RICH_AVAILABLE:
                console.print(f"\n✅ Audit completed successfully", style="green")
            else:
                print(f"\n✅ Audit completed successfully")
            sys.exit(0)
            
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n❌ Audit interrupted by user", style="red")
        else:
            print("\n❌ Audit interrupted by user")
        sys.exit(130)
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"\n❌ Error during audit: {e}", style="red")
        else:
            print(f"\n❌ Error during audit: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()