# ModPocket

A Python monorepo project organized with multiple packages.

## Structure

This repository is organized as a monorepo with the following structure:

```
ModPocket/
├── packages/
│   ├── core/           # Core functionality
│   ├── utils/          # Utility functions
│   └── api/            # API interfaces
├── pyproject.toml      # Root configuration
└── README.md           # This file
```

## Packages

- **core**: Core functionality for ModPocket
- **utils**: Utility functions and helpers
- **api**: API interfaces and endpoints

## Installation

### Installing all packages in development mode

```bash
pip install -e packages/core
pip install -e packages/utils
pip install -e packages/api
```

### Installing individual packages

You can install individual packages as needed:

```bash
pip install -e packages/core
```

## Development

### Setting up development environment

1. Clone the repository:
```bash
git clone https://github.com/TYH71/ModPocket.git
cd ModPocket
```

2. Install packages in development mode:
```bash
pip install -e packages/core[dev]
pip install -e packages/utils[dev]
pip install -e packages/api[dev]
```

### Running tests

```bash
pytest packages/
```

### Code formatting and linting

```bash
ruff check packages/
ruff format packages/
```

## Contributing

1. Create a new branch for your feature
2. Make your changes in the appropriate package
3. Ensure tests pass
4. Submit a pull request

## License

See LICENSE file for details.