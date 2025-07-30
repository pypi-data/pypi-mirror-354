# src/perch/commands/add.py

import typer
from pathlib import Path
import yaml

app = typer.Typer()

def _is_perch_project() -> bool:
    """
    Checks if the current directory is a Perch project by verifying the presence of the perch.lock file.
    """
    return Path("perch.lock").is_file()

def _integration_exists(name: str) -> bool:
    """
    Checks if an integration directory already exists.
    """
    return Path(f"integrations/{name}").is_dir()

def _check_perch_project():
    """
    Exits if the current directory is not a Perch project.
    """
    if not _is_perch_project():
        typer.secho(
            "Error: Not a Perch project. Please run 'perch init' or 'perch create <project_name>' to initialize a project (missing perch.lock).",
            fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

def _tool_exists(integration: str, entity: str) -> bool:
    return Path(f"interfaces/tools/{integration}/{entity}.py").is_file()

def _service_exists(integration: str, entity: str) -> bool:
    return Path(f"services/{integration}/{entity}.py").is_file()

def _schema_exists(integration: str, entity: str) -> bool:
    return Path(f"schemas/{integration}/{entity}.py").is_file()

def _create_tool_file(integration: str, entity: str):
    tool_file = Path(f"interfaces/tools/{integration}/{entity}.py")
    tool_file.parent.mkdir(parents=True, exist_ok=True)
    tool_file.write_text(f"""\
from core.data.tool import ToolResponse

def create_{entity}_tool() -> ToolResponse:
    return ToolResponse(status="success", message="{entity} created")
""")
    typer.echo(f"Created: {tool_file}")

def _create_service_file(integration: str, entity: str):
    service_file = Path(f"services/{integration}/{entity}.py")
    service_file.parent.mkdir(parents=True, exist_ok=True)
    service_file.write_text(f"""\
def create_{entity}():
    # This is a placeholder for your service logic.
    # It should interact with the client.
    pass
""")
    typer.echo(f"Created: {service_file}")

def _create_schema_file(integration: str, entity: str):
    schema_file = Path(f"schemas/{integration}/{entity}.py")
    schema_file.parent.mkdir(parents=True, exist_ok=True)
    schema_file.write_text(f"""\
from pydantic import BaseModel

class {entity.capitalize()}InputSchema(BaseModel):
    pass

class {entity.capitalize()}ResponseSchema(BaseModel):
    pass
""")
    typer.echo(f"Created: {schema_file}")

@app.command("integration")
def add_integration(name: str):
    """
    Adds a new integration by creating its directory structure.
    """
    _check_perch_project()
    if _integration_exists(name):
        typer.secho(f"Error: Integration '{name}' already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    paths = [
        f"integrations/{name}",
        f"interfaces/tools/{name}",
        f"interfaces/resources/{name}",
        f"schemas/{name}",
        f"services/{name}",
    ]

    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created: {path}")

    # Create client.py for the new integration
    client_file_path = Path(f"integrations/{name}/client.py")
    client_class_name = f"{name.capitalize()}Client"
    client_file_content = f"""\
class {client_class_name}:
    def __init__(self):
        pass

    def connect(self):
        # Implement connection logic here
        print(f"Connecting to {{self.__class__.__name__}}...")
        pass
"""
    client_file_path.write_text(client_file_content)
    typer.echo(f"Created: {client_file_path}")

    # Update perch.lock with the new integration
    perch_lock_path = Path("perch.lock")
    if perch_lock_path.exists():
        with open(perch_lock_path, "r") as f:
            perch_data = yaml.safe_load(f)
        
        if "integrations" not in perch_data or not isinstance(perch_data["integrations"], list):
            perch_data["integrations"] = []
        
        if name not in perch_data["integrations"]:
            perch_data["integrations"].append(name)
            with open(perch_lock_path, "w") as f:
                yaml.dump(perch_data, f, sort_keys=False)
            typer.echo(f"Updated perch.lock with integration: {name}")

@app.command("tool")
def add_tool(
    integration: str,
    entity: str,
    all_layers: bool = typer.Option(False, "--all", "-a", help="Also create service and schema files. Consider using 'perch add all' for this.")
):
    """
    Adds a new tool file for a given integration and entity.
    Optionally creates service and schema files.
    """
    _check_perch_project()
    if not _integration_exists(integration):
        typer.secho(f"Error: Integration '{integration}' not exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if _tool_exists(integration, entity):
        typer.secho(f"Error: Tool '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    _create_tool_file(integration, entity)
    if all_layers:
        if _service_exists(integration, entity):
            typer.secho(f"Error: Service '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        if _schema_exists(integration, entity):
            typer.secho(f"Error: Schema '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        _create_service_file(integration, entity)
        _create_schema_file(integration, entity)

@app.command("service")
def add_service(
    integration: str,
    entity: str
):
    """
    Adds a new service file for a given integration and entity.
    """
    _check_perch_project()
    if not _integration_exists(integration):
        typer.secho(f"Error: Integration '{integration}' not exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if _service_exists(integration, entity):
        typer.secho(f"Error: Service '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    _create_service_file(integration, entity)

@app.command("schema")
def add_schema(
    integration: str,
    entity: str
):
    """
    Adds a new schema file for a given integration and entity.
    """
    _check_perch_project()
    if not _integration_exists(integration):
        typer.secho(f"Error: Integration '{integration}' not exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if _schema_exists(integration, entity):
        typer.secho(f"Error: Schema '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    _create_schema_file(integration, entity)

@app.command("all")
def add_all(
    integration: str = typer.Argument(..., help="The name of the integration"),
    entity: str = typer.Argument(..., help="The name of the entity (e.g., user, product)")
):
    """
    Adds tool, service, and schema files for a given integration and entity.
    """
    _check_perch_project()
    if not _integration_exists(integration):
        typer.secho(f"Error: Integration '{integration}' not exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    # Check if any of the layers already exist
    if _tool_exists(integration, entity):
        typer.secho(f"Error: Tool '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if _service_exists(integration, entity):
        typer.secho(f"Error: Service '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if _schema_exists(integration, entity):
        typer.secho(f"Error: Schema '{entity}' already exists for integration '{integration}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(f"Adding all layers for integration '{integration}' and entity '{entity}'...")
    _create_tool_file(integration, entity)
    _create_service_file(integration, entity)
    _create_schema_file(integration, entity)
