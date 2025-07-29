from pathlib import Path
import typer
from renpy_assets.utils.file_utilities import find_files_by_patterns
from renpy_assets.utils.constants import ASSET_TYPES

app = typer.Typer(help="Scan Ren'Py assets like images, audio, or fonts.")

@app.command()
def scan(
    asset_type: str = typer.Argument(..., help="The asset type to scan (e.g., images, audio, fonts, video or all)."),
    path: Path = typer.Option("game", "--path", "-p", help="Directory to scan from")
):
    """
    Scan and report assets of a specified type or all types in the Ren'Py project.

    Args:
        asset_type (str): The category of assets to scan.
            Supported values: "images", "audio", "fonts", "video", "all".
        path (Path): The base directory to begin the search. Defaults to "game".

    Usage:
        renpy-assets scan images --path assets/
        renpy-assets scan all
    """
    if asset_type is None:
        typer.echo("Please provide an asset type to scan. Supported types: images, audio, fonts, all.")
        raise typer.Exit(code=1)

    if asset_type != "all" and asset_type not in ASSET_TYPES:
        typer.echo(f"Unsupported asset type: '{asset_type}'. Use one of: {', '.join(ASSET_TYPES.keys())}, all.")
        raise typer.Exit(code=1)

    resolved_path = path.resolve()
    typer.echo(f"\nScanning assets in: {resolved_path}\n")

    if asset_type == "all":
        total_found = 0
        for kind, patterns in ASSET_TYPES.items():
            typer.echo(f"{kind.capitalize()} Assets")
            results = find_files_by_patterns(str(resolved_path), patterns)
            if results:
                typer.echo(f"  Found {len(results)} {kind} asset{'s' if len(results) != 1 else ''}:")
                for file_path in results:
                    rel_path = file_path.relative_to(resolved_path)
                    typer.echo(f"    - {rel_path.as_posix()}")
                typer.echo("")  # blank line after list
                total_found += len(results)
            else:
                typer.echo(f"  No {kind} assets found.\n")
        typer.echo(f"Total assets found: {total_found}")
    else:
        patterns = ASSET_TYPES[asset_type]
        results = find_files_by_patterns(str(resolved_path), patterns)
        typer.echo(f"{asset_type.capitalize()} Assets")
        if results:
            typer.echo(f"  Found {len(results)} {asset_type} asset{'s' if len(results) != 1 else ''}:")
            for file_path in results:
                rel_path = file_path.relative_to(resolved_path)
                typer.echo(f"    - {rel_path.as_posix()}")
        else:
            typer.echo("  No matching assets found.")
