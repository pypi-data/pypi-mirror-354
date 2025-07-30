"""
Core functionality for whisper-ssh.

Contains the main RemoteNotificationManager class and related utilities.
"""

import socket
from typing import Dict, List, Optional, Tuple
import time

import validators
from fabric import Connection
from paramiko.ssh_exception import AuthenticationException, NoValidConnectionsError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import ConfigManager


class RemoteNotificationManager:
    """Main class for managing remote notifications."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the notification manager.
        
        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        self.config_manager = ConfigManager(config_file)
        self.console = Console()
    
    @property
    def config(self) -> Dict:
        """Get current configuration."""
        return self.config_manager.config
    
    def display_welcome(self) -> None:
        """Display welcome message and current stats."""
        title = Text("Remote Notification Manager", style="bold blue")
        
        stats = self.config_manager.get_stats()
        stats_text = f"""[green]✓[/green] Known Hosts: {stats['hosts']}
[green]✓[/green] Total Users: {stats['total_users']}
[green]✓[/green] Preset Messages: {stats['preset_messages']}
[cyan]📁[/cyan] Config: {self.config_manager.get_config_file_path()}"""
        
        welcome_panel = Panel(stats_text, title=title, border_style="blue")
        self.console.print(welcome_panel)
        self.console.print()
    
    def display_known_hosts(self) -> None:
        """Display table of known hosts."""
        hosts = self.config_manager.get_hosts()
        if not hosts:
            self.console.print("[yellow]No known hosts configured[/yellow]")
            return
            
        table = Table(title="Known Hosts", show_header=True, header_style="bold magenta")
        table.add_column("Hostname", style="cyan", no_wrap=True)
        table.add_column("IP Address", style="green")
        table.add_column("Known Users", style="yellow")
        
        for hostname, ip in hosts.items():
            users = self.config_manager.get_users(hostname)
            user_list = ", ".join(users) if users else "None"
            table.add_row(hostname, ip, user_list)
        
        self.console.print(table)
        self.console.print()
    
    def resolve_and_validate_host(self, host_input: str) -> Tuple[str, str]:
        """
        Resolve hostname/IP and validate connectivity.
        
        Args:
            host_input: Hostname or IP address to resolve.
            
        Returns:
            Tuple of (hostname, ip_address).
            
        Raises:
            ValueError: If host cannot be resolved.
            ConnectionError: If SSH connection test fails.
        """
        self.console.print(f"[yellow]🔍 Resolving {host_input}...[/yellow]")
        
        # Determine if input is IP or hostname
        if validators.ipv4(host_input):
            ip_address = host_input
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                self.console.print(f"[green]✓[/green] Resolved IP {ip_address} to hostname: [cyan]{hostname}[/cyan]")
            except socket.herror:
                hostname = ip_address
                self.console.print(f"[yellow]⚠[/yellow] Could not resolve hostname for {ip_address}, using IP as hostname")
        else:
            hostname = host_input
            try:
                ip_address = socket.gethostbyname(hostname)
                self.console.print(f"[green]✓[/green] Resolved hostname [cyan]{hostname}[/cyan] to IP: {ip_address}")
            except socket.gaierror as e:
                raise ValueError(f"Cannot resolve hostname '{hostname}': {e}")
        
        # Test SSH connectivity
        if self._test_ssh_connection(ip_address):
            self.console.print(f"[green]✓[/green] SSH port is reachable on {ip_address}")
        else:
            self.console.print(f"[yellow]⚠[/yellow] Cannot reach SSH port on {ip_address}")
            # Don't raise error, just warn - user might want to continue anyway
        
        # Store the mapping
        self.config_manager.add_host(hostname, ip_address)
        
        return hostname, ip_address
    
    def _test_ssh_connection(self, ip_address: str, port: int = 22, timeout: int = 5) -> bool:
        """
        Test if SSH port is reachable.
        
        Args:
            ip_address: IP address to test.
            port: SSH port (default 22).
            timeout: Connection timeout in seconds.
            
        Returns:
            True if SSH port is reachable, False otherwise.
        """
        try:
            sock = socket.create_connection((ip_address, port), timeout=timeout)
            sock.close()
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
    
    def send_notification(
        self, 
        ip_address: str, 
        username: str, 
        password: str, 
        message: str,
        title: str = "Remote Notification",
        timeout: int = 15
    ) -> bool:
        """
        Send notification to remote host using SSH.
        
        Args:
            ip_address: Target IP address.
            username: SSH username.
            password: SSH password.
            message: Notification message.
            title: Notification title (default: "Remote Notification").
            timeout: SSH connection timeout in seconds.
            
        Returns:
            True if notification was sent successfully, False otherwise.
        """
        self.console.print(f"[yellow]📤 Sending notification to {username}@{ip_address}...[/yellow]")
        
        try:
            # Create connection with password authentication
            conn = Connection(
                host=ip_address,
                user=username,
                connect_kwargs={
                    "password": password,
                    "timeout": timeout,
                    "auth_timeout": timeout,
                }
            )
            
            # Escape quotes in message for shell safety
            escaped_message = self._escape_shell_string(message)
            escaped_title = self._escape_shell_string(title)
            
            # Send notification command
            command = f'DISPLAY=:0 notify-send "{escaped_title}" "{escaped_message}"'
            
            with self.console.status("[bold yellow]Executing remote command..."):
                result = conn.run(command, hide=True, warn=True, timeout=timeout)
            
            conn.close()
            
            if result.return_code == 0:
                self.console.print("[bold green]✅ Notification sent successfully![/bold green]")
                return True
            else:
                self.console.print(f"[red]❌ Command failed with return code {result.return_code}[/red]")
                if result.stderr:
                    self.console.print(f"[red]Error: {result.stderr.strip()}[/red]")
                return False
                
        except AuthenticationException:
            self.console.print("[red]❌ Authentication failed: Invalid username or password[/red]")
            return False
        except NoValidConnectionsError:
            self.console.print("[red]❌ Connection failed: Unable to connect to host[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]❌ Unexpected error: {str(e)}[/red]")
            return False
    
    def _escape_shell_string(self, text: str) -> str:
        """
        Escape a string for safe use in shell commands.
        
        Args:
            text: Text to escape.
            
        Returns:
            Escaped text safe for shell execution.
        """
        # Replace problematic characters
        return (text
                .replace('\\', '\\\\')  # Escape backslashes first
                .replace('"', '\\"')     # Escape double quotes
                .replace('`', '\\`')     # Escape backticks
                .replace('$', '\\$'))    # Escape dollar signs
    
    def send_notification_to_multiple_hosts(
        self,
        host_configs: List[Dict[str, str]],
        message: str,
        title: str = "Remote Notification"
    ) -> Dict[str, bool]:
        """
        Send notifications to multiple hosts.
        
        Args:
            host_configs: List of dicts with 'ip', 'username', 'password' keys.
            message: Notification message.
            title: Notification title.
            
        Returns:
            Dict mapping host IPs to success status.
        """
        results = {}
        
        self.console.print(f"[cyan]📡 Sending notification to {len(host_configs)} hosts...[/cyan]")
        
        for i, config in enumerate(host_configs, 1):
            ip = config['ip']
            username = config['username']
            password = config['password']
            
            self.console.print(f"\n[cyan]({i}/{len(host_configs)})[/cyan] Processing {username}@{ip}")
            
            success = self.send_notification(ip, username, password, message, title)
            results[ip] = success
            
            # Small delay between connections to be nice to the networks
            if i < len(host_configs):
                time.sleep(0.5)
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        self.console.print(f"\n[bold]📊 Summary:[/bold]")
        self.console.print(f"[green]✅ Successful: {successful}[/green]")
        if failed > 0:
            self.console.print(f"[red]❌ Failed: {failed}[/red]")
        
        return results
    
    def test_host_connectivity(self, hostname_or_ip: str) -> Dict[str, bool]:
        """
        Test connectivity to a host.
        
        Args:
            hostname_or_ip: Hostname or IP address to test.
            
        Returns:
            Dict with test results.
        """
        results = {
            'dns_resolution': False,
            'ssh_reachable': False,
            'ping_successful': False
        }
        
        try:
            # Test DNS resolution
            if validators.ipv4(hostname_or_ip):
                # It's an IP, try reverse DNS
                try:
                    socket.gethostbyaddr(hostname_or_ip)
                    results['dns_resolution'] = True
                except socket.herror:
                    results['dns_resolution'] = False
                ip_to_test = hostname_or_ip
            else:
                # It's a hostname, try forward DNS
                try:
                    ip_to_test = socket.gethostbyname(hostname_or_ip)
                    results['dns_resolution'] = True
                except socket.gaierror:
                    results['dns_resolution'] = False
                    return results  # Can't proceed without IP
            
            # Test SSH connectivity
            results['ssh_reachable'] = self._test_ssh_connection(ip_to_test)
            
            # Test ping (basic ICMP)
            import subprocess
            import platform
            
            # Determine ping command based on OS
            ping_cmd = ["ping", "-c", "1", "-W", "3000"] if platform.system() != "Windows" else ["ping", "-n", "1", "-w", "3000"]
            ping_cmd.append(ip_to_test)
            
            try:
                result = subprocess.run(ping_cmd, capture_output=True, timeout=5)
                results['ping_successful'] = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                results['ping_successful'] = False
                
        except Exception:
            # If any unexpected error occurs, return current results
            pass
        
        return results
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        return self.config_manager.save_config()
    
    def get_config_path(self) -> str:
        """Get the path to the configuration file."""
        return str(self.config_manager.get_config_file_path())
    
    def reset_config(self) -> None:
        """Reset configuration to defaults."""
        self.config_manager.reset_config()
        self.console.print("[yellow]⚠[/yellow] Configuration reset to defaults")
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to specified path."""
        success = self.config_manager.export_config(export_path)
        if success:
            self.console.print(f"[green]✅ Configuration exported to: {export_path}[/green]")
        else:
            self.console.print(f"[red]❌ Failed to export configuration to: {export_path}[/red]")
        return success
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from specified path."""
        success = self.config_manager.import_config(import_path)
        if success:
            self.console.print(f"[green]✅ Configuration imported from: {import_path}[/green]")
        else:
            self.console.print(f"[red]❌ Failed to import configuration from: {import_path}[/red]")
        return success