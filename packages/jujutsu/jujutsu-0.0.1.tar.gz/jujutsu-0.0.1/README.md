# Jujutsu CLI 🥋

A powerful CLI tool with multiple aliases for different workflows.

## Features

- **Multiple Aliases**: Use `jujutsu`, `jutsu`, `jjz`, or `jj2` - they all work the same way!
- **Cross-Platform**: Works on Mac, Linux, and Windows
- **Easy Installation**: Available via PyPI and npm

## Installation

### From PyPI (Recommended)

```bash
pip install jujutsu
```

### From npm

```bash
npm install -g jujutsu-cli
# or use npx for one-time usage
npx jujutsu-cli --help
```

## Usage

All aliases work identically:

```bash
# Initialize a new project
jujutsu init
jutsu init
jjz init
jj2 init

# Check status
jujutsu status
jutsu status

# Show help
jujutsu help
jj2 --help

# Show version
jujutsu --version
jjz -v
```

## Available Commands

- `init` - Initialize a new project
- `status` - Show project status
- `help` - Show help information
- `--version` - Show version information

## Development

To install for development:

```bash
# Clone the repository
git clone https://github.com/dai-motoki/jujutsu.git
cd jujutsu

# Install in development mode
pip install -e .
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 