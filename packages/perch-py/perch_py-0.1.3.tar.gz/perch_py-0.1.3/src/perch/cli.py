import typer
from perch.commands import init, add

# Perch CLI - Scaffold MCP HexLayer projects
# 🌳 Perch CLI: Your tool for scaffolding MCP HexLayer projects.
#
# Next Steps:
#   - perch init: Initialize a new Perch project in the current directory.
#   - perch create: Create a new Perch project in a new directory.
#   - perch add [command]: Add components or features to your project.
app = typer.Typer(
    help="""
🌳 perch-py\n
├── init: Initialize a new Perch project in the current directory.\n
├── create: Create a new Perch project in a new directory.\n
└── add [command]: Add components or features to your project.
"""
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


# Register CLI commands
app.command("init")(init.init_current_project) # Initialize in current directory
app.command("create")(init.create_project) # Create new project in a new directory
app.add_typer(add.app, name="add", help="Add new components (integrations, tools, services, schemas) to your Perch project.")

if __name__ == "__main__":
    app()
