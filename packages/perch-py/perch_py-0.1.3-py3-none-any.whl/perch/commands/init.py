import os
import typer
import subprocess
from pathlib import Path
from typing import Optional, Any
from datetime import datetime
import uuid
import re # Import regex module

app = typer.Typer()

def _sanitize_name(name: str) -> str:
    """
    Sanitizes a name to be compatible with package/directory naming conventions.
    Converts to lowercase, replaces spaces/underscores with hyphens,
    removes invalid characters, and strips leading/trailing hyphens.
    """
    name = name.lower()
    name = re.sub(r'[_\s]+', '-', name) # Replace spaces/underscores with hyphens
    name = re.sub(r'[^a-z0-9-]', '', name) # Remove invalid characters
    name = name.strip('-') # Strip leading/trailing hyphens
    return name

def _get_gitignore_content() -> str:
    """
    Returns the standard Python .gitignore content.
    """
    return """\
# Byte-compiled / optimized / DLL files
__pycache__/
*.pyc
*.pyd
*.pyo
*.egg-info/
.pytest_cache/

# Distributions / packaging
.Python
build/
dist/
eggs/
*.egg
parts/
sdist/
var/
wheels/
*.whl
*.zip


# Environments
.env
.venv
env/
venv/
venv_*/
ENV/
env.bak/
.direnv/

# Perch specific
perch.lock
"""

def create_directories(base_path: Path, integration: str | None = None):
    dirs = [
        base_path / "core" / "data",
        base_path / "core" / "exceptions",
        base_path / "config",
        base_path / "interfaces" / "tools",
        base_path / "interfaces" / "resources",
        base_path / "interfaces" / "prompts",
        base_path / "integrations",
        base_path / "schemas",
        base_path / "services",
    ]

    if integration:
        dirs += [
            base_path / f"interfaces/tools/{integration}",
            base_path / f"interfaces/resources/{integration}",
            base_path / f"schemas/{integration}",
            base_path / f"services/{integration}",
            base_path / f"integrations/{integration}",
        ]

    for d in dirs:
        typer.echo(f"Creating directory: {d}") # Added typer.echo
        d.mkdir(parents=True, exist_ok=True)

    # Create core/data/tool.py
    typer.echo("Creating core/data/tool.py...") # Added typer.echo
    (base_path / "core" / "data" / "tool.py").write_text("""\
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ToolResponse:
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
""")

    typer.echo("Creating main.py...") # Added typer.echo
    (base_path / "main.py").write_text(f"""\
from core.server import MCPServer

if __name__ == "__main__":
    server = MCPServer(name="{base_path.name}")
    server.run()
""")

    typer.echo("Creating core/server.py...") # Added typer.echo
    (base_path / "core/server.py").write_text("""\
import importlib
import inspect
import os
from pathlib import Path # Added for path operations
import yaml # Added for perch.lock operations
from mcp.server.fastmcp import FastMCP

class MCPServer:
    def __init__(self, name: str = "Perch MCP Server"):
        self.mcp = FastMCP(name)
        self._sync_integrations_with_lock_file() # Call sync on init
        self.register_tools()

    def _sync_integrations_with_lock_file(self):
        perch_lock_path = Path("perch.lock")
        integrations_dir = Path("integrations")

        if not perch_lock_path.exists():
            print("Warning: perch.lock not found. Cannot sync integrations.")
            return

        try:
            with open(perch_lock_path, "r") as f:
                perch_data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading perch.lock: {e}")
            return

        if "integrations" not in perch_data or not isinstance(perch_data["integrations"], list):
            perch_data["integrations"] = []

        # Get integrations from file system
        fs_integrations = {d.name for d in integrations_dir.iterdir() if d.is_dir() and not d.name.startswith('__')}

        # Get integrations from perch.lock
        lock_integrations = set(perch_data["integrations"])

        new_integrations = fs_integrations - lock_integrations
        removed_integrations = lock_integrations - fs_integrations

        if new_integrations or removed_integrations:
            print("Syncing integrations in perch.lock...")
            perch_data["integrations"] = sorted(list(fs_integrations))
            try:
                with open(perch_lock_path, "w") as f:
                    yaml.dump(perch_data, f, sort_keys=False)
                if new_integrations:
                    print(f"Added new integrations to perch.lock: {', '.join(new_integrations)}")
                if removed_integrations:
                    print(f"Removed integrations from perch.lock: {', '.join(removed_integrations)}")
            except Exception as e:
                print(f"Error writing to perch.lock during sync: {e}")

    def register_tools(self, tools_path='interfaces/tools'):
        for root, _, files in os.walk(tools_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    module_path = os.path.join(root, file)
                    module_name = os.path.splitext(os.path.relpath(module_path, tools_path))[0].replace(os.sep, '.')

                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)

                    try:
                        spec.loader.exec_module(module)
                    except Exception as e:
                        print(f"❌ Failed to import {module_path}: {e}")
                        continue

                    functions = sorted(
                        inspect.getmembers(module, inspect.isfunction),
                        key=lambda item: item[0]
                    )

                    for name, func in functions:
                        if name.endswith('_tool'):
                            exposed_name = name.replace('_tool', '')
                            decorated = self.mcp.tool(name=exposed_name)(func)
                            setattr(self, exposed_name, decorated)
                            print(f"✅ Registered tool: {exposed_name}")

    def run(self, transport: str = "streamable-http"):
        self.mcp.run(transport=transport)
""")

    # Create perch.lock file
    project_id = uuid.uuid4().hex
    created_at = datetime.now().isoformat()
    project_name_for_lock = base_path.name if base_path != Path.cwd() else Path.cwd().name
    initial_integrations_list = [integration] if integration else []

    perch_lock_content = f"""\
# DO NOT DELETE THIS FILE
# Perch Project Configuration and Summary
project_name: {project_name_for_lock}
project_id: {project_id}
created_at: {created_at}
integrations:
{chr(10).join([f'  - {i}' for i in initial_integrations_list])}
"""
    (base_path / "perch.lock").write_text(perch_lock_content)

    # Create or update .gitignore file
    gitignore_path = base_path / ".gitignore"
    gitignore_content = _get_gitignore_content()

    if gitignore_path.exists():
        # Read existing content to avoid duplicating perch.lock if it's already there
        existing_content = gitignore_path.read_text()
        if "perch.lock" not in existing_content:
            with open(gitignore_path, "a") as f:
                f.write("\n" + gitignore_content)
        else:
            # If perch.lock is already there, just ensure other standard ignores are present
            # This is a simplified approach; a more robust solution might parse and merge
            # For now, we'll just overwrite if it's a new file, or append if perch.lock is missing.
            # Given the task, we'll just ensure the full content is there.
            pass # Do nothing if perch.lock already exists, assume other content is handled manually or not critical to append again.
    else:
        gitignore_path.write_text(gitignore_content)

def _generate_readme_content(project_name: str, is_normal_project: bool) -> str:
    """
    Generates the content for the README.md file.
    """
    project_type = "Normal Perch Project" if is_normal_project else "MCP Server Project"
    return f"""\
# {project_name}

## Project Description
This is a {project_type} generated by Perch CLI.

## Project Type
{project_type}

## Author
Perch CLI

## Getting Started

### Prerequisites
- Python 3.9+
- `uv` (install with `pip install uv`)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd {project_name}
   ```

2. **Activate the virtual environment:**
   ```bash
   uv venv activate
   ```

3. **Run the project:**
   ```bash
   python main.py
   ```

## Project Structure
- `config/`: Configuration files.
- `core/`: Core logic and utilities (for MCP servers, this includes `server.py`).
- `integrations/`: External service integrations.
- `interfaces/`: Definitions for tools, resources, and prompts.
- `schemas/`: Data schemas and models.
- `services/`: Business logic and service implementations.
- `main.py`: The main entry point of the application.
- `perch.lock`: Perch project lock file (DO NOT DELETE).
- `.gitignore`: Git ignore file.
- `README.md`: This project README.

## License
This project is licensed under the MIT License.
"""

@app.command("init")
def init_current_project(
    project_name: str = typer.Argument(".", help="Initialize in the current directory."),
    integration: str = typer.Option(None, "--integration", "-i", help="Optional integration name"),
    normal_project: bool = typer.Option(False, "--normal", "-n", help="Initialize as a normal project (not an MCP server).")
):
    """
    Initializes a Perch project in the current directory.
    """
    base_path = Path.cwd() # Always initialize in current working directory

    if (base_path / "perch.lock").exists() or (base_path / "pyproject.toml").exists():
        typer.secho(f"Error: Project is already initialized in '{base_path}'. Aborting.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(f"Initializing Perch project in current directory: {base_path}")

    # Pass normal_project to create_directories and perch.lock generation
    # For normal projects, core/server.py is not created, so we need to adjust create_directories
    if not normal_project:
        create_directories(base_path, integration)
    else:
        # Create only the necessary directories for a normal project
        dirs = [
            base_path / "config",
            base_path / "integrations",
            base_path / "schemas",
            base_path / "services",
        ]
        if integration:
            dirs += [
                base_path / f"schemas/{integration}",
                base_path / f"services/{integration}",
                base_path / f"integrations/{integration}",
            ]
        for d in dirs:
            typer.echo(f"Creating directory: {d}") # Added typer.echo
            d.mkdir(parents=True, exist_ok=True)

    # Create main.py based on normal_project flag
    if normal_project:
        typer.echo("Creating main.py...") # Added typer.echo
        (base_path / "main.py").write_text("""\
# This is a normal Perch project.
# You can add your Python code here.
""")
    else:
        typer.echo("Creating main.py...") # Added typer.echo
        (base_path / "main.py").write_text(f"""\
from core.server import MCPServer

if __name__ == "__main__":
    server = MCPServer(name="{base_path.name}")
    server.run()
""")

    # Create core/server.py only if not a normal project
    if not normal_project:
        typer.echo("Creating core/server.py...") # Added typer.echo
        (base_path / "core/server.py").write_text("""\
import importlib
import inspect
import os
from pathlib import Path # Added for path operations
import yaml # Added for perch.lock operations
from mcp.server.fastmcp import FastMCP

class MCPServer:
    def __init__(self, name: str = "Perch MCP Server"):
        self.mcp = FastMCP(name)
        self._sync_integrations_with_lock_file() # Call sync on init
        self.register_tools()

    def _sync_integrations_with_lock_file(self):
        perch_lock_path = Path("perch.lock")
        integrations_dir = Path("integrations")

        if not perch_lock_path.exists():
            print("Warning: perch.lock not found. Cannot sync integrations.")
            return

        try:
            with open(perch_lock_path, "r") as f:
                perch_data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading perch.lock: {e}")
            return

        if "integrations" not in perch_data or not isinstance(perch_data["integrations"], list):
            perch_data["integrations"] = []

        # Get integrations from file system
        fs_integrations = {d.name for d in integrations_dir.iterdir() if d.is_dir() and not d.name.startswith('__')}

        # Get integrations from perch.lock
        lock_integrations = set(perch_data["integrations"])

        new_integrations = fs_integrations - lock_integrations
        removed_integrations = lock_integrations - fs_integrations

        if new_integrations or removed_integrations:
            print("Syncing integrations in perch.lock...")
            perch_data["integrations"] = sorted(list(fs_integrations))
            try:
                with open(perch_lock_path, "w") as f:
                    yaml.dump(perch_data, f, sort_keys=False)
                if new_integrations:
                    print(f"Added new integrations to perch.lock: {', '.join(new_integrations)}")
                if removed_integrations:
                    print(f"Removed integrations from perch.lock: {', '.join(removed_integrations)}")
            except Exception as e:
                print(f"Error writing to perch.lock during sync: {e}")

    def register_tools(self, tools_path='interfaces/tools'):
        for root, _, files in os.walk(tools_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    module_path = os.path.join(root, file)
                    module_name = os.path.splitext(os.path.relpath(module_path, tools_path))[0].replace(os.sep, '.')

                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)

                    try:
                        spec.loader.exec_module(module)
                    except Exception as e:
                        print(f"❌ Failed to import {module_path}: {e}")
                        continue

                    functions = sorted(
                        inspect.getmembers(module, inspect.isfunction),
                        key=lambda item: item[0]
                    )

                    for name, func in functions:
                        if name.endswith('_tool'):
                            exposed_name = name.replace('_tool', '')
                            decorated = self.mcp.tool(name=exposed_name)(func)
                            setattr(self, exposed_name, decorated)
                            print(f"✅ Registered tool: {exposed_name}")

    def run(self, transport: str = "streamable-http"):
        self.mcp.run(transport=transport)
""")

    # Create perch.lock file
    project_id = uuid.uuid4().hex
    created_at = datetime.now().isoformat()
    project_name_for_lock = base_path.name # Always use current directory name for init

    # Adjust project_name_for_lock based on normal_project flag
    if not normal_project and not project_name_for_lock.endswith("-mcp-server"):
        project_name_for_lock += "-mcp-server"
    elif normal_project and (project_name_for_lock.endswith("-mcp-server") or project_name_for_lock.endswith("-mcp")):
        # Remove any MCP suffix for normal projects
        project_name_for_lock = project_name_for_lock.replace("-mcp-server", "").replace("-mcp", "")

    initial_integrations_list = [integration] if integration else []

    perch_lock_content = f"""\
# DO NOT DELETE THIS FILE
# Perch Project Configuration and Summary
project_name: {project_name_for_lock}
project_id: {project_id}
created_at: {created_at}
integrations:
{chr(10).join([f'  - {i}' for i in initial_integrations_list])}
"""
    (base_path / "perch.lock").write_text(perch_lock_content)

    # Create or update .gitignore file
    gitignore_path = base_path / ".gitignore"
    gitignore_content = _get_gitignore_content()

    if gitignore_path.exists():
        existing_content = gitignore_path.read_text()
        if "perch.lock" not in existing_content: # Check if perch.lock is already in the existing .gitignore
            with open(gitignore_path, "a") as f:
                f.write("\n" + gitignore_content)
        else:
            # If perch.lock is already there, ensure other standard ignores are present.
            # For simplicity, we'll just overwrite if it's a new file, or append if perch.lock is missing.
            # A full merge is out of scope for this task.
            pass # Do nothing if perch.lock already exists, assume other content is handled manually or not critical to append again.
    else:
        gitignore_path.write_text(gitignore_content)

    # Run uv commands in the current directory
    typer.echo("\n\n📦 Initializing Python environment and installing dependencies...")
    # `uv init .` initializes the project and creates the virtual environment.
    # `uv venv` is called explicitly as requested, though it might be redundant after `uv init .`.
    subprocess.run(["uv", "init", "."], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["uv", "venv"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # The `source .venv/bin/activate` command is a shell built-in and cannot directly activate
    # the environment for the current Python script's process or subsequent `subprocess.run` calls
    # in the same way it does for a user's shell. `uv` commands automatically use the local
    # `.venv` for dependency management, so explicit activation within the script is not needed
    # for `uv add` to function correctly.
    if not normal_project:
        subprocess.run(["uv", "add", "mcp[cli]"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["uv", "add", "pydantic"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["uv", "add", "pyyaml"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Add pyyaml dependency
        subprocess.run(["uv", "add", "PyYAML"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Add PyYAML dependency for YAML handling
        subprocess.run(["uv", "add", "perch-py"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    else:
        # Add perch-py as a dependency for normal projects
        subprocess.run(["uv", "add", "perch-py"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    typer.secho("✅ Packages initialized!", fg=typer.colors.GREEN)

    typer.secho("\n🎉 Project initialized successfully!", fg=typer.colors.GREEN)
    typer.echo("\nNext steps:")
    typer.echo("  1. Activate the virtual environment:")
    typer.echo("     source .venv/bin/activate") # Modified activation instruction
    typer.echo("  2. Run the project:")
    typer.echo("     python main.py")

    # Handle README.md generation
    readme_path = base_path / "README.md"
    if readme_path.exists() and readme_path.read_text().strip():
        typer.secho("README.md already exists and has content. Skipping generation.", fg=typer.colors.YELLOW)
    else:
        readme_content = _generate_readme_content(base_path.name, normal_project)
        readme_path.write_text(readme_content)
        typer.secho("README.md generated successfully.", fg=typer.colors.BLUE)


@app.command("create")
def create_project(
    project_name: str = typer.Argument(..., help="The name of the new project directory."),
    integration: str = typer.Option(None, "--integration", "-i", help="Optional integration name"),
    normal_project: bool = typer.Option(False, "--normal", "-n", help="Create as a normal project (not an MCP server).")
):
    """
    Creates a new Perch project in a new directory.
    """
    if project_name == ".":
        typer.secho("Error: 'perch create' is for new directories. Use 'perch init' to initialize in the current directory.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    sanitized_project_name = _sanitize_name(project_name)
    if not sanitized_project_name:
        typer.secho("Error: Project name cannot be empty or contain only invalid characters.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Adjust project name suffix based on normal_project flag
    final_project_name = sanitized_project_name
    if not normal_project:
        # Default behavior: MCP server project, must be suffixed with -mcp-server
        if not final_project_name.endswith("-mcp-server"):
            final_project_name += "-mcp-server"
    else:
        # Normal project: exact name, no suffixing
        # _sanitize_name already applied, so just use it as is
        pass
    
    # Final check for valid start/end characters after sanitization and suffixing
    if not re.match(r'^[a-z0-9].*[a-z0-9]$', final_project_name):
        typer.secho(f"Error: Sanitized project name '{final_project_name}' must start and end with a letter or digit.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    base_path = Path.cwd() / final_project_name

    # Check if the directory exists and is already a Perch project
    if base_path.exists():
        if (base_path / "perch.lock").exists() or (base_path / "pyproject.toml").exists():
            typer.secho(f"❌ Error: Project is already initialized in '{base_path}'. Aborting.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        else:
            # Directory exists but is not a Perch project, proceed with initialization
            typer.echo(f"⚠️ Warning: Directory '{final_project_name}' already exists but is not a Perch project. Proceeding with initialization.")
    
    # Create the base project directory (if it doesn't exist or if it's an empty/non-Perch existing dir)
    base_path.mkdir(parents=True, exist_ok=True)
    
    typer.echo(f"✨ Creating new project: {final_project_name}")

    # Create directories based on normal_project flag
    if not normal_project:
        create_directories(base_path, integration)
    else:
        # Create only the necessary directories for a normal project
        dirs = [
            base_path / "config",
            base_path / "integrations",
            base_path / "schemas",
            base_path / "services",
        ]
        if integration:
            dirs += [
                base_path / f"schemas/{integration}",
                base_path / f"services/{integration}",
                base_path / f"integrations/{integration}",
            ]
        for d in dirs:
            typer.echo(f"Creating directory: {d}") # Added typer.echo
            d.mkdir(parents=True, exist_ok=True)

    # Create main.py based on normal_project flag
    if normal_project:
        typer.echo("Creating main.py...") # Added typer.echo
        (base_path / "main.py").write_text("""\
# This is a normal Perch project.
# You can add your Python code here.
""")
    else:
        typer.echo("Creating main.py...") # Added typer.echo
        (base_path / "main.py").write_text(f"""\
from core.server import MCPServer

if __name__ == "__main__":
    server = MCPServer(name="{final_project_name}")
    server.run()
""")

    # Create core/server.py only if not a normal project
    if not normal_project:
        typer.echo("Creating core/server.py...") # Added typer.echo
        (base_path / "core/server.py").write_text("""\
import importlib
import inspect
import os
from pathlib import Path # Added for path operations
import yaml # Added for perch.lock operations
from mcp.server.fastmcp import FastMCP

class MCPServer:
    def __init__(self, name: str = "Perch MCP Server"):
        self.mcp = FastMCP(name)
        self._sync_integrations_with_lock_file() # Call sync on init
        self.register_tools()

    def _sync_integrations_with_lock_file(self):
        perch_lock_path = Path("perch.lock")
        integrations_dir = Path("integrations")

        if not perch_lock_path.exists():
            print("Warning: perch.lock not found. Cannot sync integrations.")
            return

        try:
            with open(perch_lock_path, "r") as f:
                perch_data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading perch.lock: {e}")
            return

        if "integrations" not in perch_data or not isinstance(perch_data["integrations"], list):
            perch_data["integrations"] = []

        # Get integrations from file system
        fs_integrations = {d.name for d in integrations_dir.iterdir() if d.is_dir() and not d.name.startswith('__')}

        # Get integrations from perch.lock
        lock_integrations = set(perch_data["integrations"])

        new_integrations = fs_integrations - lock_integrations
        removed_integrations = lock_integrations - fs_integrations

        if new_integrations or removed_integrations:
            print("Syncing integrations in perch.lock...")
            perch_data["integrations"] = sorted(list(fs_integrations))
            try:
                with open(perch_lock_path, "w") as f:
                    yaml.dump(perch_data, f, sort_keys=False)
                if new_integrations:
                    print(f"Added new integrations to perch.lock: {', '.join(new_integrations)}")
                if removed_integrations:
                    print(f"Removed integrations from perch.lock: {', '.join(removed_integrations)}")
            except Exception as e:
                print(f"Error writing to perch.lock during sync: {e}")

    def register_tools(self, tools_path='interfaces/tools'):
        for root, _, files in os.walk(tools_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    module_path = os.path.join(root, file)
                    module_name = os.path.splitext(os.path.relpath(module_path, tools_path))[0].replace(os.sep, '.')

                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)

                    try:
                        spec.loader.exec_module(module)
                    except Exception as e:
                        print(f"❌ Failed to import {module_path}: {e}")
                        continue

                    functions = sorted(
                        inspect.getmembers(module, inspect.isfunction),
                        key=lambda item: item[0]
                    )

                    for name, func in functions:
                        if name.endswith('_tool'):
                            exposed_name = name.replace('_tool', '')
                            decorated = self.mcp.tool(name=exposed_name)(func)
                            setattr(self, exposed_name, decorated)
                            print(f"✅ Registered tool: {exposed_name}")

    def run(self, transport: str = "streamable-http"):
        self.mcp.run(transport=transport)
""")

    # Create perch.lock file
    project_id = uuid.uuid4().hex
    created_at = datetime.now().isoformat()
    project_name_for_lock = final_project_name # Use the final project name for perch.lock

    initial_integrations_list = [integration] if integration else []

    perch_lock_content = f"""\
# DO NOT DELETE THIS FILE
# Perch Project Configuration and Summary
project_name: {project_name_for_lock}
project_id: {project_id}
created_at: {created_at}
integrations:
{chr(10).join([f'  - {i}' for i in initial_integrations_list])}
"""
    (base_path / "perch.lock").write_text(perch_lock_content)

    # Create or update .gitignore file
    gitignore_path = base_path / ".gitignore"
    gitignore_content = _get_gitignore_content()

    if gitignore_path.exists():
        existing_content = gitignore_path.read_text()
        if "perch.lock" not in existing_content: # Check if perch.lock is already in the existing .gitignore
            with open(gitignore_path, "a") as f:
                f.write("\n" + gitignore_content)
        else:
            # If perch.lock is already there, ensure other standard ignores are present.
            # For simplicity, we'll just overwrite if it's a new file, or append if perch.lock is missing.
            # A full merge is out of scope for this task.
            pass # Do nothing if perch.lock already exists, assume other content is handled manually or not critical to append again.
    else:
        gitignore_path.write_text(gitignore_content)

    # Change directory and run uv commands in the new project directory
    os.chdir(base_path)
    typer.echo("📦 Initializing Python environment and installing dependencies...") # Added typer.echo
    # `uv init .` initializes the project and creates the virtual environment.
    # `uv venv` is called explicitly as requested, though it might be redundant after `uv init .`.
    subprocess.run(["uv", "init", "."], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["uv", "venv"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # The `source .venv/bin/activate` command is a shell built-in and cannot directly activate
    # the environment for the current Python script's process or subsequent `subprocess.run` calls
    # in the same way it does for a user's shell. `uv` commands automatically use the local
    # `.venv` for dependency management, so explicit activation within the script is not needed
    # for `uv add` to function correctly.
    if not normal_project:
        subprocess.run(["uv", "add", "mcp[cli]"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["uv", "add", "pydantic"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["uv", "add", "pyyaml"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["uv", "add", "PyYAML"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # For normal projects, add perch-py as a dependency
        subprocess.run(["uv", "add", "perch-py"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    typer.secho("✅ Packages initialized!", fg=typer.colors.GREEN) # Added typer.secho

    # Handle README.md generation
    readme_path = base_path / "README.md"
    if readme_path.exists() and readme_path.read_text().strip():
        typer.secho("⚠️ README.md already exists and has content. Skipping generation.", fg=typer.colors.YELLOW)
    else:
        readme_content = _generate_readme_content(final_project_name, normal_project)
        readme_path.write_text(readme_content)
        typer.secho("📄 README.md generated successfully.", fg=typer.colors.BLUE)

    typer.secho("\n🎉 Perch project created! You're off to a flying start!", fg=typer.colors.GREEN)
    typer.echo(f"\n\n🌳 Next steps 🌳:\n\n➡️  cd {final_project_name}")
    typer.echo("➡️  Activate the virtual environment:")
    typer.echo("    source .venv/bin/activate") # Modified activation instruction
    typer.echo("➡️  Run the project:")
    typer.echo("    python main.py\n")

    # Log initial integration if provided
    if integration:
        typer.echo(f"\n🔗 Initial integration '{integration}' added to project.\n")

    # Change back to the original directory after creating the project
    os.chdir("..")
