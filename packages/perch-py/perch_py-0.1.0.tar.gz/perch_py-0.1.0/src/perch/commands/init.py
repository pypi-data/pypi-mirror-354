import os
import typer
import subprocess

app = typer.Typer()

def create_directories(project_name: str, integration: str | None = None):
    base = Path(project_name)

    dirs = [
        base / "core" / "data",
        base / "core" / "exceptions",
        base / "config",
        base / "interfaces" / "tools",
        base / "interfaces" / "resources",
        base / "interfaces" / "prompts",
        base / "integrations",
        base / "schemas",
        base / "services",
    ]

    if integration:
        dirs += [
            base / f"interfaces/tools/{integration}",
            base / f"interfaces/resources/{integration}",
            base / f"schemas/{integration}",
            base / f"services/{integration}",
            base / f"integrations/{integration}",
        ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    (base / "main.py").write_text("""\
from core.server import MCPServer

if __name__ == "__main__":
    server = MCPServer(name="My New MCP Server")
    server.run()
""")

    (base / "core/server.py").write_text("""\
import importlib
import inspect
import os
from mcp.server.fastmcp import FastMCP

class MCPServer:
    def __init__(self, name: str = "Perch MCP Server"):
        self.mcp = FastMCP(name)
        self.register_tools()

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

    # Initialize uv and install dependencies
    os.chdir(base)
    subprocess.run(["uv", "init", "."], check=False)
    subprocess.run(["uv", "add", "mcp[cli]"], check=False)
    subprocess.run(["uv", "add", "pydantic"], check=False)

@app.command()
def init_project(
    project_name: str,
    integration: str = typer.Option(None, "--integration", "-i", help="Optional integration name")
):
    typer.echo(f"Creating new project: {project_name}")
    create_directories(project_name, integration)

    typer.secho("\nProject created!", fg=typer.colors.GREEN)
    typer.echo(f"\nNext steps:\n  cd {project_name}")
    typer.echo("  uv venv activate")
    typer.echo("  python main.py")
