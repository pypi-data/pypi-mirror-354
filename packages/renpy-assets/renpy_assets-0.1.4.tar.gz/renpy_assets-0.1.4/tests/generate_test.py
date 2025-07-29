from pathlib import Path
from typer.testing import CliRunner
from renpy_assets.commands.generate import app

runner = CliRunner()

def setup_test_files(base: Path, files: list[str]):
    for file in files:
        path = base / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("dummy content")


def test_generate_images(tmp_path):
    setup_test_files(tmp_path, ["images/bg/scene 1.png", "images/sprite.webp"])
    output_file = tmp_path / "images_decls.rpy"

    result = runner.invoke(app, ["images", "--path", str(tmp_path), "--output", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert "# --- Image Assets ---" in content
    assert 'image scene_1 = "images/bg/scene 1.png"' in content
    assert 'image sprite = "images/sprite.webp"' in content

    assert "Generating declarations" in result.stdout
    assert "Total declarations written: 2" in result.stdout


def test_generate_images_with_spaces(tmp_path):
    setup_test_files(tmp_path, ["images/bg/scene_1.png", "images/sprite.webp"])
    output_file = tmp_path / "images_spaces.rpy"

    result = runner.invoke(app, [
        "images", "--path", str(tmp_path), "--output", str(output_file), "--spaces"
    ])

    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert "# --- Image Assets ---" in content
    assert 'image scene 1 = "images/bg/scene_1.png"' in content
    assert 'image sprite = "images/sprite.webp"' in content


def test_generate_audio(tmp_path):
    setup_test_files(tmp_path, ["audio/music/theme.ogg", "audio/sfx/click.mp3"])
    output_file = tmp_path / "audio_decls.rpy"

    result = runner.invoke(app, ["audio", "-p", str(tmp_path), "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert "# --- Audio Assets ---" in content
    assert 'define audio.theme = "audio/music/theme.ogg"' in content
    assert 'define audio.click = "audio/sfx/click.mp3"' in content


def test_generate_fonts(tmp_path):
    setup_test_files(tmp_path, ["fonts/main/Font-Regular.ttf", "fonts/title.otf"])
    output_file = tmp_path / "fonts_decls.rpy"

    result = runner.invoke(app, ["fonts", "-p", str(tmp_path), "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert "# --- Font Assets ---" in content
    assert 'define font_regular_font = "fonts/main/Font-Regular.ttf"' in content
    assert 'define title_font = "fonts/title.otf"' in content


def test_generate_all(tmp_path):
    setup_test_files(tmp_path, [
        "images/img.png",
        "audio/snd.wav",
        "fonts/font.ttf",
    ])
    output_file = tmp_path / "all_decls.rpy"

    result = runner.invoke(app, ["all", "-p", str(tmp_path), "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert "# --- Image Assets ---" in content
    assert "# --- Audio Assets ---" in content
    assert "# --- Font Assets ---" in content

    assert 'image img = "images/img.png"' in content
    assert 'define audio.snd = "audio/snd.wav"' in content
    assert 'define font_font = "fonts/font.ttf"' in content

    assert "Total declarations written: 3" in result.stdout


def test_generate_no_assets(tmp_path):
    output_file = tmp_path / "empty.rpy"

    result = runner.invoke(app, ["images", "--path", str(tmp_path), "--output", str(output_file)])

    assert result.exit_code == 0
    assert not output_file.exists()
    assert "No matching assets found to generate declarations." in result.stdout


def test_generate_invalid_asset_type(tmp_path):
    result = runner.invoke(app, ["videos", "--path", str(tmp_path)])

    assert result.exit_code == 1
    assert "Unsupported asset type" in result.stdout
