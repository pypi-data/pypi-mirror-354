# Perch - MCP HexLayer Scaffolding CLI

Perch is a developer-friendly command-line tool for scaffolding and managing [MCP HexLayer Architecture](https://github.com/modelcontextprotocol/python-sdk) server projects.

It helps you build modular, maintainable MCP servers using clean structure and naming conventions based on primarily on CGUDL (Create, Get, Update, Delete, List), but you can use ACTION type naming conventions.

---

## Features

- Scaffold full MCP HexLayer projects
- Add integrations, tools, services, and schemas
- Works with [uv](https://github.com/astral-sh/uv)
- Built with [Typer](https://typer.tiangolo.com)

---

## Installation

To install Perch, use pip:

```bash
pip install perch-py
```

For more details, visit the [Perch-Py PyPI page](https://pypi.org/project/perch-py/).

---

## Usage

Perch provides commands to initialize new projects, create new projects in separate directories, and add various components (integrations, tools, services, schemas) to an existing project.

### Initialize Project in Current Directory (`perch init`)

Initializes a Perch project in the current working directory.

```bash
perch init
```

With an optional integration:

```bash
perch init --integration github
```

To initialize a project where the `-mcp-server` suffix is not enforced on the project name:

```bash
perch init --normal # Note: Not Recommended
```

### Create New Project (`perch create`)

Creates a new Perch project in a new directory. By default, if no `--normal` flag is used, the project name for an MCP server will be strictly suffixed with `-mcp-server` (e.g., `my-server` becomes `my-server-mcp-server`).

```bash
perch create my-mcp-server
```

With an optional integration:

```bash
perch create my-mcp-server --integration github
```

To create a project where the `-mcp-server` suffix is not enforced on the project name:

```bash
perch create my-normal-project --normal # Note: Not Recommended
```

### After Project Initialization/Creation

After `perch init` or `perch create`, navigate into your project directory and activate the virtual environment:

```bash
cd my-mcp-server # or my-normal-project
uv venv activate
python main.py
```

### Add Commands (`perch add`)

The `perch add` command is used to add various components to an existing Perch project.

#### Add Integration (`perch add integration`)

Adds a new integration by creating its directory structure and a `client.py` file.

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
integrations/github/client.py
```

And the content of `integrations/github/client.py`:

```python
# integrations/github/client.py
class GithubClient:
    def __init__(self):
        pass

    def connect(self):
        # Implement connection logic here
        print(f"Connecting to {self.__class__.__name__}...")
        pass
```

#### Add Tool (`perch add tool`)

Adds a new tool file for a given integration and entity.

```bash
perch add tool github user
```

Creates:

```python
# interfaces/tools/github/user.py
from core.data.tool import ToolResponse
from pydantic import Field
from schemas.github.user import UserInputSchema, UserResponseSchema
from services.github.user import create_user

def create_user_tool(
    sample1: str = Field(..., description="The sample1 of the user."),
    sample2: str = Field(..., description="The sample2 of the user.")
) -> ToolResponse:
    """
    Creates a new user with the provided sample1 and sample2.
    """
    user = create_user(UserInputSchema.model_validate({"sample1": sample1, "sample2": sample2}))
    if not user:
        return ToolResponse(status="error", message="User creation failed.")

    return ToolResponse(
        status="success",
        message="User created successfully",
        data=UserResponseSchema.model_validate(user)
    )
```

#### Add Service (`perch add service`)

Adds a new service file for a given integration and entity.

```bash
perch add service github user
```

Creates:

```python
# services/github/user.py
from schemas.github.user import UserInputSchema, UserResponseSchema
import uuid
import datetime

def create_user(input_data: UserInputSchema) -> UserResponseSchema:
    # Example Process
    item = {
        "sample1": input_data.sample1,
        "sample2": input_data.sample2,
    }
    return UserResponseSchema(**item)
```

#### Add Schema (`perch add schema`)

Adds a new schema file for a given integration and entity.

```bash
perch add schema github user
```

Creates:

```python
# schemas/github/user.py
from pydantic import BaseModel
from typing import Optional

class UserInputSchema(BaseModel):
    sample1: str
    sample2: str

class UserResponseSchema(BaseModel):
    sample1: str
    sample2: str
    # Add other fields as necessary, e.g., id, created_at
```

#### Add All Layers (`perch add all`)

Adds tool, service, and schema files for a given integration and entity in one go.

```bash
perch add all github user
```

Creates:

```python
# interfaces/tools/github/user.py
# services/github/user.py
# schemas/github/user.py
```

---

## Constraints and Flags

Perch commands often support flags to modify their behavior.

- **`--integration` (`-i`)**: Used to specify an initial integration when creating or initializing a project.
- **`--normal` (`-n`)**: This flag allows you to create a _standard Python project_ instead of an MCP server project. When used, Perch will scaffold a basic Python project structure without the MCP-specific server components. For projects created with `--normal`, the `-mcp-server` suffix is _not_ enforced on the project name, allowing for more flexible naming for non-MCP projects.

* **Naming Convention for MCP Server Projects**: By default, when creating an MCP server project (i.e., without the `--normal` flag), Perch strictly enforces that the project directory name ends with `-mcp-server`. For example, if you run `perch create my-server`, the created directory will be `my-server-mcp-server`. This suffix is mandatory for all MCP server projects to ensure consistency and clear identification.

---

## Architecture Explanation

### Overview

Perch is designed to facilitate the development of MCP HexLayer Architecture servers. It promotes a clean, modular structure by separating concerns into distinct layers: integrations, interfaces (tools, resources, prompts), schemas, and services. This approach, inspired by the Hexagonal Architecture (Ports and Adapters) and primarily based on CGUDL (Create, Get, Update, Delete, List) principles, ensures maintainability, testability, and scalability. The name "Perch" signifies this elevated and clear perspective that clean architecture provides over system layers.

### Detailed Architecture

For a comprehensive explanation of the MCP HexLayer Architecture, please refer to the [MCP Python SDK repository](https://github.com/modelcontextprotocol/python-sdk).

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

## Local Development

### Installation

add git clone then cd or etc.

To set up Perch for local development:

```bash
uv pip install -e .
```

Then, you can run the CLI:

```bash
perch --help
```

### Uninstall

```bash
uv pip uninstall perch-py
```

### Reinstall After Edits

```bash
uv pip install -e .
```

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
