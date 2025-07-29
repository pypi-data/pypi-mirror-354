import typer
from renpy_assets.commands import scan, generate

app = typer.Typer(help="renpy-assets: CLI to manage Ren'Py project assets.")

# Register subcommands
app.add_typer(scan.app, help="Scan for Ren'Py assets")
app.add_typer(generate.app, help="Generate declarations for assets")

if __name__ == "__main__":
    app()
