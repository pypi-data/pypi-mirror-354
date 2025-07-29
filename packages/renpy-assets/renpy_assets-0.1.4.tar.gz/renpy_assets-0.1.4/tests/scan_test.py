from pathlib import Path
from typer.testing import CliRunner
from renpy_assets.commands.scan import app

runner = CliRunner()

def setup_test_files(base: Path, files: list[str]):
    for file in files:
        path = base / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("dummy content")

def test_scan_images(tmp_path):
    setup_test_files(tmp_path, ["bg/scene1.png", "sprites/charA.webp", "menu.jpg"])

    result = runner.invoke(app, ["images", "--path", str(tmp_path)])

    assert result.exit_code == 0
    # Matches the prettier output
    assert "Images Assets" in result.stdout
    assert "Found 3 images assets" in result.stdout or "Found 3 image assets" in result.stdout
    assert "bg/scene1.png" in result.stdout
    assert "sprites/charA.webp" in result.stdout
    assert "menu.jpg" in result.stdout

def test_scan_audio(tmp_path):
    setup_test_files(tmp_path, ["sfx/click.ogg", "music/theme.mp3", "voice/line.wav"])

    result = runner.invoke(app, ["audio", "-p", str(tmp_path)])

    assert result.exit_code == 0
    assert "Audio Assets" in result.stdout
    assert "Found 3 audio assets" in result.stdout or "Found 3 audio asset" in result.stdout
    assert "sfx/click.ogg" in result.stdout
    assert "music/theme.mp3" in result.stdout
    assert "voice/line.wav" in result.stdout

def test_scan_fonts(tmp_path):
    setup_test_files(tmp_path, ["fonts/main.ttf", "fonts/title.otf"])

    result = runner.invoke(app, ["fonts", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Fonts Assets" in result.stdout
    assert "Found 2 fonts assets" in result.stdout or "Found 2 font assets" in result.stdout
    assert "fonts/main.ttf" in result.stdout
    assert "fonts/title.otf" in result.stdout

def test_scan_invalid_asset_type(tmp_path):
    result = runner.invoke(app, ["videos", "--path", str(tmp_path)])

    assert result.exit_code == 1
    assert "Unsupported asset type" in result.stdout

def test_scan_no_assets_found(tmp_path):
    # No files created in tmp_path
    result = runner.invoke(app, ["images", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Images Assets" in result.stdout
    assert "No matching assets found." in result.stdout

def test_scan_all(tmp_path):
    setup_test_files(tmp_path, [
        "bg/scene1.png", "sprites/charA.webp",
        "sfx/click.ogg", "music/theme.mp3",
        "fonts/main.ttf"
    ])

    result = runner.invoke(app, ["all", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Images Assets" in result.stdout
    assert "Audio Assets" in result.stdout
    assert "Fonts Assets" in result.stdout

    assert "Found 2 images assets" in result.stdout or "Found 2 image assets" in result.stdout
    assert "Found 2 audio assets" in result.stdout or "Found 2 audio asset" in result.stdout
    assert "Found 1 fonts asset" in result.stdout or "Found 1 font asset" in result.stdout

    assert "bg/scene1.png" in result.stdout
    assert "sprites/charA.webp" in result.stdout
    assert "sfx/click.ogg" in result.stdout
    assert "music/theme.mp3" in result.stdout
    assert "fonts/main.ttf" in result.stdout

    assert "Total assets found: 5" in result.stdout
