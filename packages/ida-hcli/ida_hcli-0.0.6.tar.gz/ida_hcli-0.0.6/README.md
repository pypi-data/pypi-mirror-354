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

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Report bugs
- Suggest features  
- Submit pull requests
- Set up your development environment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Issues and Support

- **Bug Reports & Feature Requests**: [GitHub Issues](https://github.com/hexrays/ida-hcli/issues)
- **Questions & Discussions**: [GitHub Discussions](https://github.com/hexrays/ida-hcli/discussions)
- **Commercial Support**: Contact support@hex-rays.com
- **Hex-Rays Website**: [hex-rays.com](https://hex-rays.com/)

## Development

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/hexrays/ida-hcli.git
cd ida-hcli

# Install dependencies
uv sync

# Run in development mode
uv run hcli --help
```

### Testing

```bash
# Run tests
uv run pytest

# Test CLI commands
uv run hcli whoami
uv run hcli plugin list
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.