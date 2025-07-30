# ida-hcli

A command-line interface for managing IDA Pro licenses, plugins, and cloud services.

## Installation

Install using `uv`:

```bash
# Install globally
uvx ida-hcli

# Or install as a tool
uv tool install ida-hcli
```

## Quick Start

```bash
# Login to your Hex-Rays account
hcli login

# Check your authentication status
hcli whoami

# Browse and install plugins
hcli plugin browse
hcli plugin install <plugin-name>

# Manage your licenses
hcli license list

# Use cloud analysis
hcli cloud analyze <binary-file>
```

## Commands

- **Authentication**: `hcli login`, `hcli logout`, `hcli whoami`
- **Plugin Management**: `hcli plugin list|search|install|uninstall|browse`
- **License Management**: `hcli license list|get|install`
- **Cloud Services**: `hcli cloud analyze`, `hcli cloud session list`
- **File Sharing**: `hcli share put|get|list|delete`
- **IDA Configuration**: `hcli ida config get|set|list|delete`

## Configuration

The CLI stores configuration in your system's standard config directory:
- Linux/macOS: `~/.config/hcli/`
- Windows: `%APPDATA%\hcli\`

Set environment variables for advanced configuration:
- `HCLI_API_KEY`: Use API key authentication instead of OAuth
- `HCLI_DEBUG`: Enable debug output
- `HCLI_API_URL`: Override default API endpoint

## Support

For issues and feature requests, visit the [Hex-Rays website](https://hex-rays.com/) or contact support@hex-rays.com.