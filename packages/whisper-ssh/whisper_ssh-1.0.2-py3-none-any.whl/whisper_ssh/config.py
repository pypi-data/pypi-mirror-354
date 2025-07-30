"""
Configuration management for whisper-ssh.

Handles loading, saving, and managing configuration data including
hosts, users, and preset messages.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import os


class ConfigManager:
    """Manages configuration data for remote notifications."""
    
    DEFAULT_CONFIG_NAME = "whisper_ssh_config.json"
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to config file. If None, uses default location.
        """
        if config_file is None:
            # Use user's home directory for system-wide installation
            config_dir = Path.home() / ".config" / "whisper-ssh"
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_file = config_dir / self.DEFAULT_CONFIG_NAME
        else:
            self.config_file = Path(config_file)
        
        self.config = self._load_or_create_config()
    
    def _load_or_create_config(self) -> Dict:
        """Load configuration from file or create default config."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Ensure all required keys exist
                    return self._validate_and_update_config(config)
            except (json.JSONDecodeError, IOError, KeyError) as e:
                print(f"Warning: Error loading config ({e}), creating new one")
                return self._create_default_config()
        else:
            config = self._create_default_config()
            self.save_config()
            return config
    
    def _validate_and_update_config(self, config: Dict) -> Dict:
        """Validate and update config structure if needed."""
        default_config = self._create_default_config()
        
        # Ensure all required top-level keys exist
        for key in default_config:
            if key not in config:
                config[key] = default_config[key]
        
        # Validate data types
        if not isinstance(config.get('hosts'), dict):
            config['hosts'] = {}
        if not isinstance(config.get('users'), dict):
            config['users'] = {}
        if not isinstance(config.get('preset_messages'), list):
            config['preset_messages'] = default_config['preset_messages']
        
        return config
    
    def _create_default_config(self) -> Dict:
        """Create default configuration structure."""
        return {
            "hosts": {},
            "users": {},
            "preset_messages": [
                "System maintenance starting in 30 minutes",
                "Please save your work and log off",
                "Server will reboot in 10 minutes", 
                "Network maintenance in progress",
                "Meeting starting in 5 minutes",
                "Lunch break is over - back to work!",
                "Don't forget to backup your work",
                "System update completed successfully",
                "Build completed successfully",
                "Deployment finished",
                "Backup process completed",
                "Security update available"
            ]
        }
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_hosts(self) -> Dict[str, str]:
        """Get all known hosts."""
        return self.config.get('hosts', {}).copy()
    
    def add_host(self, hostname: str, ip_address: str) -> None:
        """Add or update a host mapping."""
        self.config['hosts'][hostname] = ip_address
    
    def remove_host(self, hostname: str) -> bool:
        """
        Remove a host and its associated users.
        
        Returns:
            True if host was removed, False if not found.
        """
        if hostname in self.config['hosts']:
            del self.config['hosts'][hostname]
            # Also remove users for this host
            if hostname in self.config['users']:
                del self.config['users'][hostname]
            return True
        return False
    
    def get_users(self, hostname: str) -> List[str]:
        """Get known users for a specific host."""
        return self.config.get('users', {}).get(hostname, []).copy()
    
    def add_user(self, hostname: str, username: str) -> None:
        """Add a user to a host's user list."""
        if hostname not in self.config['users']:
            self.config['users'][hostname] = []
        if username not in self.config['users'][hostname]:
            self.config['users'][hostname].append(username)
    
    def remove_user(self, hostname: str, username: str) -> bool:
        """
        Remove a user from a host's user list.
        
        Returns:
            True if user was removed, False if not found.
        """
        if hostname in self.config['users'] and username in self.config['users'][hostname]:
            self.config['users'][hostname].remove(username)
            # Clean up empty user lists
            if not self.config['users'][hostname]:
                del self.config['users'][hostname]
            return True
        return False
    
    def get_preset_messages(self) -> List[str]:
        """Get all preset messages."""
        return self.config.get('preset_messages', []).copy()
    
    def add_preset_message(self, message: str) -> None:
        """Add a new preset message."""
        if message not in self.config['preset_messages']:
            self.config['preset_messages'].append(message)
    
    def remove_preset_message(self, message: str) -> bool:
        """
        Remove a preset message.
        
        Returns:
            True if message was removed, False if not found.
        """
        if message in self.config['preset_messages']:
            self.config['preset_messages'].remove(message)
            return True
        return False
    
    def get_config_file_path(self) -> Path:
        """Get the path to the configuration file."""
        return self.config_file
    
    def reset_config(self) -> None:
        """Reset configuration to defaults."""
        self.config = self._create_default_config()
        self.save_config()
    
    def export_config(self, export_path: str) -> bool:
        """
        Export configuration to a specific file.
        
        Args:
            export_path: Path where to export the config.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """
        Import configuration from a specific file.
        
        Args:
            import_path: Path to import the config from.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                print(f"Import file does not exist: {import_path}")
                return False
                
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validate imported config
            self.config = self._validate_and_update_config(imported_config)
            self.save_config()
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error importing config: {e}")
            return False
    
    def get_stats(self) -> Dict[str, int]:
        """Get configuration statistics."""
        return {
            'hosts': len(self.config.get('hosts', {})),
            'total_users': sum(len(users) for users in self.config.get('users', {}).values()),
            'preset_messages': len(self.config.get('preset_messages', [])),
        }