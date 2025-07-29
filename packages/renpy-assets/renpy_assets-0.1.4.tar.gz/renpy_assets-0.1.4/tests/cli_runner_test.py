import tempfile
from pathlib import Path
from typer.testing import CliRunner
from renpy_assets.cli import app

runner = CliRunner()

def test_generate_command():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        output_file = base / "generated_assets.rpy"

        # Create dummy image files
        (base / "bg_menu.png").write_text("dummy")
        (base / "hero.png").write_text("dummy")

        result = runner.invoke(
            app,
            [
                "generate", "images",
                "--path", str(base),
                "--output", str(output_file)
            ]
        )

        print("\nCOMMAND OUTPUT:", result.stdout)  # Add this
        print("ERROR OUTPUT:", result.stderr)     # Add this
        print("EXCEPTION:", result.exception)  

        assert result.exit_code == 0
        assert "2 declaration" in result.stdout
        assert f"Output saved to: {output_file.resolve()}" in result.stdout

        assert output_file.exists()
        content = output_file.read_text()
        assert 'image bg_menu = "bg_menu.png"' in content
        assert 'image hero = "hero.png"' in content
