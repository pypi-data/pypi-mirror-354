import typer
from perch.commands import init, add

app = typer.Typer(help="Perch CLI - Scaffold MCP HexLayer projects")

# Register CLI commands
app.command("init")(init.init_current_project) # Initialize in current directory
app.command("create")(init.create_project) # Create new project in a new directory
app.add_typer(add.app, name="add")

if __name__ == "__main__":
    app()
