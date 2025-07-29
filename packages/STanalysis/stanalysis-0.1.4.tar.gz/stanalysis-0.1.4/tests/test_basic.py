import tomli
from pathlib import Path
from STanalysis import __version__


def test_version():
    # Read version from pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    
    expected_version = pyproject["project"]["version"]
    assert __version__ == expected_version, f"Version mismatch: {__version__} != {expected_version}"
