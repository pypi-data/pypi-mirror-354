import tempfile
from pathlib import Path
from renpy_assets.commands.generate import find_files_by_patterns

def test_find_files_by_patterns():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        # Create test files
        (base / "test1.png").write_text("dummy")
        (base / "test2.mp3").write_text("dummy")
        (base / "not_an_image.txt").write_text("dummy")

        # Search for images
        patterns = [r".*\.png$"]
        found = find_files_by_patterns(str(base), patterns)
        assert len(found) == 1
        assert (base / "test1.png") in found
