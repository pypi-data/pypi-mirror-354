"""
Command-line interface for whisper-ssh.

Provides interactive CLI for sending remote notifications.
"""

import sys
from typing import List, Optional

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .core import RemoteNotificationManager
from . import __version__


class RemoteNotifyCLI:
    """Command-line interface for remote notifications."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize CLI with optional config file."""
        self.manager = RemoteNotificationManager(config_file)
        self.console = Console()
        
        # Custom questionary style
        self.style = questionary.Style([
            ('question', 'bold'),
            ('answer', 'fg:#ff9d00 bold'),
            ('pointer', 'fg:#ff9d00 bold'),
            ('highlighted', 'fg:#ff9d00 bold'),
            ('selected', 'fg:#cc5454'),
            ('separator', 'fg:#cc5454'),
            ('instruction', ''),
            ('text', ''),
        ])
    
    def get_host_selection(self) -> str:
        """Get host selection from user with menu interface."""
        hosts = self.manager.config_manager.get_hosts()
        choices = []
        
        # Add existing hosts
        for hostname, ip in hosts.items():
            choices.append(f"{hostname} ({ip})")
        
        # Add option for new host
        choices.append("➕ Enter new hostname/IP")
        
        if choices[:-1]:  # If we have existing hosts, show them
            self.manager.display_known_hosts()
        
        choice = questionary.select(
            "Select target host:",
            choices=choices,
            style=self.style
        ).ask()
        
        if choice is None:  # User cancelled
            raise KeyboardInterrupt
        
        if choice == "➕ Enter new hostname/IP":
            return self._prompt_for_new_host()
        else:
            # Extract hostname from "hostname (ip)" format
            return choice.split(' (')[0]
    
    def _prompt_for_new_host(self) -> str:
        """Prompt user for new hostname or IP address."""
        host_input = questionary.text(
            "Enter hostname or IP address:",
            validate=lambda x: len(x.strip()) > 0 or "Please enter a valid hostname or IP",
            style=self.style
        ).ask()
        
        if host_input is None:
            raise KeyboardInterrupt
            
        return host_input.strip()
    
    def get_user_selection(self, hostname: str) -> str:
        """Get username selection for the specified host."""
        users = self.manager.config_manager.get_users(hostname)
        choices = users.copy() if users else []
        choices.append("➕ Enter new username")
        
        if len(choices) > 1:  # If we have existing users
            self.console.print(f"[cyan]Known users for {hostname}:[/cyan] {', '.join(choices[:-1])}")
        
        choice = questionary.select(
            f"Select username for {hostname}:",
            choices=choices,
            style=self.style
        ).ask()
        
        if choice is None:
            raise KeyboardInterrupt
        
        if choice == "➕ Enter new username":
            new_user = questionary.text(
                "Enter username:",
                validate=lambda x: len(x.strip()) > 0 or "Username cannot be empty",
                style=self.style
            ).ask()
            
            if new_user is None:
                raise KeyboardInterrupt
            
            # Add to known users for this host
            self.manager.config_manager.add_user(hostname, new_user)
            return new_user
        else:
            return choice
    
    def get_message_selection(self) -> str:
        """Get message selection from user."""
        preset_messages = self.manager.config_manager.get_preset_messages()
        choices = preset_messages.copy()
        choices.extend(["➕ Enter custom message", "📝 Manage preset messages"])
        
        choice = questionary.select(
            "Select message to send:",
            choices=choices,
            style=self.style
        ).ask()
        
        if choice is None:
            raise KeyboardInterrupt
        
        if choice == "➕ Enter custom message":
            custom_message = questionary.text(
                "Enter your custom message:",
                validate=lambda x: len(x.strip()) > 0 or "Message cannot be empty",
                style=self.style
            ).ask()
            
            if custom_message is None:
                raise KeyboardInterrupt
            
            # Ask if user wants to save this message
            save_choice = questionary.confirm(
                "Save this message for future use?",
                style=self.style
            ).ask()
            
            if save_choice:
                self.manager.config_manager.add_preset_message(custom_message)
                self.console.print("[green]✓[/green] Message saved to presets")
            
            return custom_message
        
        elif choice == "📝 Manage preset messages":
            return self._manage_preset_messages()
        
        else:
            return choice
    
    def _manage_preset_messages(self) -> str:
        """Manage preset messages (add/remove)."""
        while True:
            action = questionary.select(
                "Manage preset messages:",
                choices=[
                    "📋 View all messages",
                    "➕ Add new message",
                    "🗑️ Remove message",
                    "↩️ Back to message selection"
                ],
                style=self.style
            ).ask()
            
            if action is None or action == "↩️ Back to message selection":
                return self.get_message_selection()
            
            elif action == "📋 View all messages":
                self._display_preset_messages()
            
            elif action == "➕ Add new message":
                new_message = questionary.text(
                    "Enter new preset message:",
                    validate=lambda x: len(x.strip()) > 0 or "Message cannot be empty",
                    style=self.style
                ).ask()
                
                if new_message:
                    self.manager.config_manager.add_preset_message(new_message)
                    self.console.print("[green]✓[/green] Message added to presets")
            
            elif action == "🗑️ Remove message":
                preset_messages = self.manager.config_manager.get_preset_messages()
                if not preset_messages:
                    self.console.print("[yellow]No preset messages to remove[/yellow]")
                    continue
                
                msg_to_remove = questionary.select(
                    "Select message to remove:",
                    choices=preset_messages,
                    style=self.style
                ).ask()
                
                if msg_to_remove:
                    confirm = questionary.confirm(
                        f"Remove '{msg_to_remove}'?",
                        style=self.style
                    ).ask()
                    
                    if confirm:
                        self.manager.config_manager.remove_preset_message(msg_to_remove)
                        self.console.print("[green]✓[/green] Message removed")
    
    def _display_preset_messages(self):
        """Display all preset messages in a table."""
        from rich.table import Table
        
        preset_messages = self.manager.config_manager.get_preset_messages()
        if not preset_messages:
            self.console.print("[yellow]No preset messages configured[/yellow]")
            return
        
        table = Table(title="Preset Messages", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Message", style="white")
        
        for i, message in enumerate(preset_messages, 1):
            table.add_row(str(i), message)
        
        self.console.print(table)
        self.console.print()
    
    def get_password(self) -> str:
        """Get SSH password securely."""
        password = questionary.password(
            "Enter SSH password:",
            style=self.style
        ).ask()
        
        if password is None:
            raise KeyboardInterrupt
            
        return password
    
    def show_main_menu(self) -> str:
        """Show main menu and return user choice."""
        choices = [
            "📤 Send notification",
            "📋 View configuration",
            "🔧 Manage hosts",
            "📝 Manage messages", 
            "🧪 Test connectivity",
            "⚙️ Configuration tools",
            "❌ Exit"
        ]
        
        choice = questionary.select(
            "What would you like to do?",
            choices=choices,
            style=self.style
        ).ask()
        
        return choice or "❌ Exit"
    
    def run_interactive(self):
        """Run interactive CLI mode."""
        try:
            self.manager.display_welcome()
            
            while True:
                choice = self.show_main_menu()
                
                if choice == "📤 Send notification":
                    self._send_notification_workflow()
                elif choice == "📋 View configuration":
                    self._view_configuration()
                elif choice == "🔧 Manage hosts":
                    self._manage_hosts()
                elif choice == "📝 Manage messages":
                    self._manage_preset_messages()
                elif choice == "🧪 Test connectivity":
                    self._test_connectivity()
                elif choice == "⚙️ Configuration tools":
                    self._configuration_tools()
                elif choice == "❌ Exit":
                    break
                
                # Pause between operations
                self.console.print()
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled by user[/yellow]")
    
    def _send_notification_workflow(self):
        """Complete workflow for sending a notification."""
        try:
            # Get host selection and resolve
            selected_host = self.get_host_selection()
            hostname, ip_address = self.manager.resolve_and_validate_host(selected_host)
            
            # Get user selection
            username = self.get_user_selection(hostname)
            
            # Get password
            password = self.get_password()
            
            # Get message
            message = self.get_message_selection()
            
            # Send notification
            success = self.manager.send_notification(ip_address, username, password, message)
            
            if success:
                # Save configuration updates
                self.manager.save_config()
                
                # Display success summary
                summary_panel = Panel(
                    f"""[green]✓[/green] Notification sent successfully!
                    
[bold]Host:[/bold] {hostname} ({ip_address})
[bold]User:[/bold] {username}
[bold]Message:[/bold] {message}""",
                    title="[green]Success[/green]",
                    border_style="green"
                )
                self.console.print(summary_panel)
            else:
                self.console.print("[red]Failed to send notification. Please check your credentials and try again.[/red]")
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled[/yellow]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def _view_configuration(self):
        """Display current configuration."""
        self.manager.display_known_hosts()
        self._display_preset_messages()
        
        stats = self.manager.config_manager.get_stats()
        config_path = self.manager.get_config_path()
        
        info_panel = Panel(
            f"""[cyan]Configuration File:[/cyan] {config_path}
[cyan]Total Hosts:[/cyan] {stats['hosts']}
[cyan]Total Users:[/cyan] {stats['total_users']}
[cyan]Preset Messages:[/cyan] {stats['preset_messages']}""",
            title="Configuration Info",
            border_style="cyan"
        )
        self.console.print(info_panel)
    
    def _manage_hosts(self):
        """Host management menu."""
        while True:
            action = questionary.select(
                "Manage hosts:",
                choices=[
                    "📋 View all hosts",
                    "➕ Add new host",
                    "🗑️ Remove host",
                    "🧪 Test host connectivity",
                    "↩️ Back to main menu"
                ],
                style=self.style
            ).ask()
            
            if action is None or action == "↩️ Back to main menu":
                break
            elif action == "📋 View all hosts":
                self.manager.display_known_hosts()
            elif action == "➕ Add new host":
                self._add_host_manually()
            elif action == "🗑️ Remove host":
                self._remove_host()
            elif action == "🧪 Test host connectivity":
                self._test_connectivity()
    
    def _add_host_manually(self):
        """Manually add a host."""
        try:
            host_input = self._prompt_for_new_host()
            hostname, ip_address = self.manager.resolve_and_validate_host(host_input)
            self.manager.save_config()
            self.console.print(f"[green]✓[/green] Host added: {hostname} ({ip_address})")
        except (ValueError, KeyboardInterrupt) as e:
            if isinstance(e, ValueError):
                self.console.print(f"[red]Error: {e}[/red]")
    
    def _remove_host(self):
        """Remove a host from configuration."""
        hosts = self.manager.config_manager.get_hosts()
        if not hosts:
            self.console.print("[yellow]No hosts to remove[/yellow]")
            return
        
        host_choices = [f"{hostname} ({ip})" for hostname, ip in hosts.items()]
        choice = questionary.select(
            "Select host to remove:",
            choices=host_choices,
            style=self.style
        ).ask()
        
        if choice:
            hostname = choice.split(' (')[0]
            confirm = questionary.confirm(f"Remove host '{hostname}'?", style=self.style).ask()
            
            if confirm:
                self.manager.config_manager.remove_host(hostname)
                self.manager.save_config()
                self.console.print(f"[green]✓[/green] Host '{hostname}' removed")
    
    def _test_connectivity(self):
        """Test connectivity to a host."""
        try:
            host_input = self._prompt_for_new_host()
            self.console.print(f"[yellow]🧪 Testing connectivity to {host_input}...[/yellow]")
            
            results = self.manager.test_host_connectivity(host_input)
            
            # Display results
            from rich.table import Table
            table = Table(title=f"Connectivity Test: {host_input}")
            table.add_column("Test", style="cyan")
            table.add_column("Result", style="white")
            
            for test, success in results.items():
                status = "[green]✓ Pass[/green]" if success else "[red]✗ Fail[/red]"
                table.add_row(test.replace('_', ' ').title(), status)
            
            self.console.print(table)
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Test cancelled[/yellow]")
    
    def _configuration_tools(self):
        """Configuration management tools."""
        while True:
            action = questionary.select(
                "Configuration tools:",
                choices=[
                    "📤 Export configuration",
                    "📥 Import configuration", 
                    "🔄 Reset to defaults",
                    "📍 Show config location",
                    "↩️ Back to main menu"
                ],
                style=self.style
            ).ask()
            
            if action is None or action == "↩️ Back to main menu":
                break
            elif action == "📤 Export configuration":
                self._export_config()
            elif action == "📥 Import configuration":
                self._import_config()
            elif action == "🔄 Reset to defaults":
                self._reset_config()
            elif action == "📍 Show config location":
                self.console.print(f"[cyan]Configuration file:[/cyan] {self.manager.get_config_path()}")
    
    def _export_config(self):
        """Export configuration to file."""
        export_path = questionary.text(
            "Enter export path:",
            default="remote_notify_backup.json",
            style=self.style
        ).ask()
        
        if export_path:
            self.manager.export_config(export_path)
    
    def _import_config(self):
        """Import configuration from file."""
        import_path = questionary.text(
            "Enter import path:",
            style=self.style
        ).ask()
        
        if import_path:
            self.manager.import_config(import_path)
    
    def _reset_config(self):
        """Reset configuration to defaults."""
        confirm = questionary.confirm(
            "This will reset all configuration to defaults. Continue?",
            style=self.style
        ).ask()
        
        if confirm:
            self.manager.reset_config()


def main():
    """Main entry point for the CLI application."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Whisper messages to remote Linux machines via SSH")
    parser.add_argument("--version", action="version", version=f"whisper-ssh {__version__}")
    parser.add_argument("--config", help="Path to configuration file")
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        cli = RemoteNotifyCLI(config_file=args.config)
        
        # For now, always run in interactive mode
        cli.run_interactive()
            
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]👋 Goodbye![/yellow]")
    except Exception as e:
        console = Console()
        console.print(f"[red]💥 Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()