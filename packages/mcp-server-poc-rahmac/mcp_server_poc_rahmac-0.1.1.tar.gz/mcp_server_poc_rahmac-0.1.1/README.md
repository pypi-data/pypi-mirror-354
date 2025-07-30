# MCP Server Example

A simple Python-based MCP (Model Context Protocol) Server that demonstrates the basic capabilities of an MCP server.

## Features

This MCP server provides:

### Tools
- **greeting**: Generate personalized greetings with different styles
- **calculator**: Perform basic arithmetic operations (add, subtract, multiply, divide)

### Resources
- **sample://users**: A list of sample user data
- **sample://products**: A list of sample product data

### Prompts
- **code_review**: Generate code review checklists for different programming languages and complexity levels

## Installation

### From PyPI
```bash
pip install mcp-server-poc-rahmac
```

### From Source
```bash
git clone https://github.com/rahmac/mcp_poc.git
cd mcp_poc
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/rahmac/mcp_poc.git
cd mcp_poc
pip install -e ".[dev]"
```

## Usage

### Running the Server

The server can be run directly:
```bash
mcp-server-poc-rahmac
```

Or using Python:
```bash
python -m mcp_server_example.server
```

### Using with MCP Clients

This server implements the MCP protocol and can be used with any MCP-compatible client. The server communicates via stdio.

#### Example Configuration

For MCP clients that use configuration files:

```json
{
  "servers": {
    "example": {
      "command": "mcp-server-poc-rahmac",
      "args": []
    }
  }
}
```

## API Reference

### Tools

#### greeting
Generate a personalized greeting.

**Parameters:**
- `name` (string, required): The name of the person to greet
- `greeting_type` (string, optional): Type of greeting - "hello", "hi", or "howdy" (default: "hello")

**Example:**
```json
{
  "name": "greeting",
  "arguments": {
    "name": "Alice",
    "greeting_type": "hi"
  }
}
```

#### calculator
Perform basic arithmetic operations.

**Parameters:**
- `operation` (string, required): The operation - "add", "subtract", "multiply", or "divide"
- `a` (number, required): First number
- `b` (number, required): Second number

**Example:**
```json
{
  "name": "calculator",
  "arguments": {
    "operation": "add",
    "a": 5,
    "b": 3
  }
}
```

### Resources

#### sample://users
Returns a JSON array of sample user objects with id, name, and email fields.

#### sample://products
Returns a JSON array of sample product objects with id, name, and price fields.

### Prompts

#### code_review
Generate a code review checklist.

**Parameters:**
- `language` (string, required): Programming language
- `complexity` (string, optional): Complexity level - "basic", "intermediate", or "advanced" (default: "intermediate")

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/rahmac/mcp_poc.git
cd mcp_poc

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/
```

### Building for PyPI

```bash
# Build the package
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*
```


## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## Changelog

### 0.1.0 (2024-06-10)
- Initial release
- Basic MCP server implementation
- Greeting and calculator tools
- Sample resources
- Code review prompt

