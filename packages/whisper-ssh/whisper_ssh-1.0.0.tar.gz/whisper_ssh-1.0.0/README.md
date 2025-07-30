# 📡 Remote Notify

[![PyPI version](https://badge.fury.io/py/remote-notify.svg)](https://badge.fury.io/py/remote-notify)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Send desktop notifications to remote Linux machines via SSH with a beautiful, interactive command-line interface.

## ✨ Features

- 🎯 **Smart Host Management** - Automatic DNS resolution and SSH connectivity testing
- 👤 **User Management** - Remember users per host for quick selection
- 💬 **Flexible Messaging** - Preset messages plus custom message support
- 🔒 **Secure** - No password storage, secure SSH connections
- 🎨 **Beautiful Interface** - Rich terminal UI with colors and interactive menus
- 📦 **Easy Installation** - One command pip install
- ⚡ **Fast Setup** - Auto-configuring with sensible defaults

## 🚀 Quick Start

### Installation

```bash
pip install remote-notify
```

### Usage

```bash
# Interactive mode (recommended)
remote-notify

# Or use the short alias
rnotify
```

### First Run

The tool will guide you through:

1. **Select Target Host** - Choose from known hosts or add a new one
2. **DNS Resolution** - Automatic hostname/IP resolution and validation
3. **Choose User** - Select from previous users or add new
4. **Enter Password** - Secure password input (never stored)
5. **Pick Message** - Choose from presets or write custom message
6. **Send!** - Notification appears on remote desktop

## 🎯 Use Cases

- **System Administration** - Notify users about maintenance, reboots, updates
- **Development Teams** - Notify about build completions, deployments
- **Remote Work** - Send meeting reminders, break notifications
- **Automation** - Integrate with scripts and monitoring systems

## 📖 Examples

### Basic Usage (Interactive)

```bash
$ remote-notify
```

### Programmatic Usage

```python
from remote_notify import RemoteNotificationManager

manager = RemoteNotificationManager()

# Send a notification
success = manager.send_notification(
    ip_address="192.168.1.100",
    username="john",
    password="secret",
    message="Build completed successfully!",
    title="CI/CD Pipeline"
)

if success:
    print("Notification sent!")
```

### Multiple Hosts

```python
# Send to multiple hosts at once
host_configs = [
    {"ip": "192.168.1.100", "username": "user1", "password": "pass1"},
    {"ip": "192.168.1.101", "username": "user2", "password": "pass2"},
]

results = manager.send_notification_to_multiple_hosts(
    host_configs=host_configs,
    message="System maintenance in 30 minutes",
    title="System Notice"
)
```

## 🔧 Configuration

Configuration is automatically stored in `~/.config/remote-notify/remote_notify_config.json`

### Configuration Structure

```json
{
  "hosts": {
    "server1": "192.168.1.100",
    "workstation": "10.0.0.50"
  },
  "users": {
    "server1": ["admin", "developer"],
    "workstation": ["user"]
  },
  "preset_messages": [
    "System maintenance starting in 30 minutes",
    "Please save your work and log off",
    "Meeting starting in 5 minutes"
  ]
}
```

### Built-in Preset Messages

- System maintenance notifications
- Reboot warnings
- Meeting reminders
- Break notifications
- Build/deployment status
- Security updates

## 🛠️ Requirements

### Local Machine

- Python 3.7+
- Network access to target machines

### Target Machines (Remote)

- Ubuntu/Linux with desktop environment
- SSH server running
- `libnotify-bin` package installed:
  ```bash
  sudo apt install libnotify-bin
  ```
- User logged into desktop session

## 🎨 Interface Features

### Interactive Menus

- ✅ Arrow key navigation
- ✅ Searchable host/user lists
- ✅ Colored output and status indicators
- ✅ Progress bars and loading indicators
- ✅ Error handling with helpful messages

### Management Features

- 📋 View all configuration
- ➕ Add/remove hosts and users
- 📝 Manage preset messages
- 🧪 Test connectivity
- 📤 Export/import configuration
- 🔄 Reset to defaults

## 🔒 Security

- **No Password Storage** - Passwords are never saved to disk
- **SSH Security** - Uses Fabric's secure SSH implementation
- **Input Validation** - Prevents shell injection attacks
- **Connection Testing** - Validates hosts before attempting connections

## 🐛 Troubleshooting

### Common Issues

**"Connection failed"**

- Verify SSH is running: `sudo systemctl status ssh`
- Check firewall: `sudo ufw status`
- Test manual connection: `ssh user@host`

**"Cannot resolve hostname"**

- Check DNS settings
- Try using IP address instead
- Verify network connectivity

**"Notification doesn't appear"**

- Ensure user is logged into desktop
- Check if Do Not Disturb is enabled
- Verify notify-send is installed: `which notify-send`

### Debug Mode

```python
# Enable verbose SSH output
manager = RemoteNotificationManager()
# Set hide=False in send_notification for debugging
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/remote-notify.git
cd remote-notify

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black remote_notify/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Fabric](https://www.fabfile.org/) - High-level SSH library
- [Questionary](https://github.com/tmbo/questionary) - Interactive CLI prompts
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output
- [Validators](https://github.com/kvesteri/validators) - Input validation

## 🔗 Links

- **PyPI**: https://pypi.org/project/remote-notify/
- **GitHub**: https://github.com/JdMasuta/remote-notify
- **Issues**: https://github.com/JdMasuta/remote-notify/issues
- **Documentation**: https://github.com/JdMasuta/remote-notify#readme
