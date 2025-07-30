# Perch - MCP HexLayer Scaffolding CLI

Perch is a developer-friendly command-line tool for scaffolding and managing [MCP HexLayer Architecture](https://github.com/modelcontextprotocol/python-sdk) server projects.

It helps you build modular, maintainable MCP servers using clean structure and naming conventions based on CGUDL (Create, Get, Update, Delete, List).

---

## Features

- Scaffold full MCP HexLayer projects
- Add integrations, tools, services, and schemas
- `-a` flag to auto-generate full service/schema stack
- Works with [uv](https://github.com/astral-sh/uv)
- Built with [Typer](https://typer.tiangolo.com)

---

## Installation (Local Development)

```bash
uv pip install -e .
```

Then:

```bash
perch --help
```

---

## Usage

### Create a New Project

```bash
perch my-mcp-server
```

With an integration:

```bash
perch my-mcp-server --integration github
```

---

### After Init

```bash
cd my-mcp-server
uv venv activate
python main.py
```

---

## Add Commands

### Add Integration

```bash
perch add integration github
```

Creates:

```
integrations/github/
interfaces/tools/github/
interfaces/resources/github/
schemas/github/
services/github/
```

---

### Add Tool

```bash
perch add tool github user
```

Creates:

```python
# interfaces/tools/github/user.py
def create_user_tool():
    pass
```

With `-a` flag:

```bash
perch add tool -a github user
```

Also creates:

```python
# services/github/user.py
def create_user():
    pass

# schemas/github/user.py
from pydantic import BaseModel

class CreateUserInputSchema(BaseModel):
    pass

class UserResponseSchema(BaseModel):
    pass
```

---

### Add Schema

```bash
perch add schema github issue
```

Creates:

```python
from pydantic import BaseModel

class CreateIssueInputSchema(BaseModel):
    pass

class IssueResponseSchema(BaseModel):
    pass
```

---

### Add Service

```bash
perch add service github user
```

Creates:

```python
# services/github/user.py
def create_user():
    pass
```

---

## Example Project Structure

```
my-mcp-server/
├── main.py
├── core/
│   ├── server.py
│   └── data/
│       └── tool.py
├── config/
├── integrations/
│   └── github/
├── interfaces/
│   ├── tools/
│   │   └── github/
│   ├── resources/
│   │   └── github/
│   └── prompts/
├── schemas/
│   └── github/
├── services/
│   └── github/
└── .venv/
```

---

## Development Notes

### Uninstall

```bash
uv pip uninstall perch-py
```

### Reinstall After Edits

```bash
uv pip install -e .
```

---

## About the Name

Perch represents a clean, elevated perspective — just like how clean architecture gives you clarity and control over your system layers.

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
