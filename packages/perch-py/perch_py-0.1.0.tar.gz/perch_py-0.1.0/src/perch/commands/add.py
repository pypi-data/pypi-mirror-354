# src/perch/commands/add.py

import typer
from pathlib import Path

app = typer.Typer()

@app.command("integration")
def add_integration(name: str):
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

@app.command("tool")
def add_tool(
    integration: str,
    entity: str,
    all_layers: bool = typer.Option(False, "--all", "-a", help="Also create service and schema files")
):
    tool_file = Path(f"interfaces/tools/{integration}/{entity}.py")
    tool_file.parent.mkdir(parents=True, exist_ok=True)
    tool_file.write_text(f"""\
from core.data.tool import ToolResponse

def create_{entity}_tool() -> ToolResponse:
    return ToolResponse(status="success", message="{entity} created")
""")

    typer.echo(f"Created: {tool_file}")

    if all_layers:
        service_file = Path(f"services/{integration}/{entity}.py")
        schema_file = Path(f"schemas/{integration}/{entity}.py")

        service_file.parent.mkdir(parents=True, exist_ok=True)
        schema_file.parent.mkdir(parents=True, exist_ok=True)

        service_file.write_text(f"""\
def create_{entity}():
    pass
""")

        schema_file.write_text(f"""\
from pydantic import BaseModel

class Create{entity.capitalize()}InputSchema(BaseModel):
    pass

class {entity.capitalize()}ResponseSchema(BaseModel):
    pass
""")

        typer.echo(f"Created: {service_file}")
        typer.echo(f"Created: {schema_file}")
