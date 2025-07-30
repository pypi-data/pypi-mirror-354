"""Basic test to verify the EOMS package structure."""

import sys
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_package_imports():
    """Test that basic package imports work."""
    # This will import from src/__init__.py
    import src

    assert hasattr(src, "__version__")
    assert src.__version__ == "1.0.0"


def test_directory_structure():
    """Test that required directories exist."""
    repo_root = Path(__file__).parent.parent

    assert (repo_root / "src").exists()
    assert (repo_root / "tests").exists()
    assert (repo_root / "plugins").exists()

    # Check for __init__.py files
    assert (repo_root / "src" / "__init__.py").exists()
    assert (repo_root / "tests" / "__init__.py").exists()
    assert (repo_root / "plugins" / "__init__.py").exists()
