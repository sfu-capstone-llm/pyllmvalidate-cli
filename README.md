# PyllmValidate CLI

A command-line tool for validating code patches using AI. This tool analyzes git diffs and provides AI-powered feedback on code correctness and quality.

## Features

- **Git Integration**: Automatically analyzes git diffs and staged changes
- **AI-Powered Validation**: Uses local AI models (via LM Studio) to validate code changes
- **Linting Context**: Optional integration with Ruff for additional code quality checks
- **Modular Architecture**: Clean separation between validation logic and target code

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pyllmvalidate-cli
```

2. Install dependencies:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

Run the tool in a git repository with unstaged changes:

```bash
python main.py
```

### With Linting Context

Include Ruff linting results in the analysis:

```bash
python main.py --lint-context
```

### Environment Configuration

Specify environment settings:

```bash
python main.py --env production
```

## Project Structure

```
pyllmvalidate-cli/
├── src/                          # The validation tool source
│   └── pyllmvalidate/
│       ├── __init__.py
│       ├── cli.py                # Command-line interface
│       ├── validators/
│       │   ├── __init__.py
│       │   └── core.py           # Core validation models
│       └── utils/
│           ├── __init__.py
│           ├── git_utils.py      # Git operations
│           ├── ai_utils.py       # AI client operations
│           └── lint_utils.py     # Linting utilities
├── examples/                     # Target code examples
│   ├── basic_project/
│   │   ├── main.py
│   │   ├── math_operations.py
│   │   └── __init__.py
│   └── advanced_project/
├── tests/                        # Tests for the tool
│   ├── unit/
│   │   ├── test_validators.py
│   │   └── test_cli.py
│   ├── integration/
│   └── fixtures/                 # Test target code
│       ├── valid_code/
│       └── invalid_code/
├── docs/
├── pyproject.toml
├── README.md
└── .gitignore
```

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Code Formatting

```bash
ruff format .
```

### Linting

```bash
ruff check .
```

## Configuration

The tool is configured to work with LM Studio running locally on port 1234. You can modify the AI client configuration in `src/pyllmvalidate/utils/ai_utils.py`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request
