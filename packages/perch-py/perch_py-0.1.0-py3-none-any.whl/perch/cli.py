import typer
from perch.commands import init, add

app = typer.Typer(help="Perch CLI - Scaffold MCP HexLayer projects")

# Register CLI commands
app.command()(init.init_project)
app.add_typer(add.app, name="add")

if __name__ == "__main__":
    app()
