"""Tests for the run_script function."""
import os
import tempfile

from chaeto.cli import extract_python_version, parse_script_requirements, run_script


def test_parse_script_requirements():
    """Test parsing script requirements from comments."""
    # Create a temporary script file with requirements
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write("""
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "numpy==2.2.3",
#     "polars==1.30.0",
# ]
# ///

print("Hello, world!")
""")
        script_path = f.name

    try:
        # Test parsing requirements
        python_version_constraint, dependencies = parse_script_requirements(script_path)
        assert python_version_constraint == ">=3.12"
        assert "numpy==2.2.3" in dependencies
        assert "polars==1.30.0" in dependencies
        assert len(dependencies) == 2
    finally:
        # Clean up
        os.unlink(script_path)


def test_extract_python_version():
    """Test extracting Python version from version constraints."""
    assert extract_python_version(">=3.12") == "3.12"
    assert extract_python_version("==3.11") == "3.11"
    assert extract_python_version(">3.10,<3.13") == "3.10"
    assert extract_python_version("invalid") == "3.12"  # Default


def test_run_script_nonexistent():
    """Test running a nonexistent script."""
    result = run_script("nonexistent_script.py")
    assert result == 1


def test_run_script_real(monkeypatch):
    """Test running a real script with mocked subprocess calls."""
    # Create a temporary script file
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write("""
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "numpy==2.2.3",
# ]
# ///

print("Hello, world!")
""")
        script_path = f.name

    # Mock subprocess.run to avoid actually creating venvs and running scripts
    def mock_run(*args, **kwargs):
        class Result:
            returncode = 0
            stdout = b""
            stderr = b""
        return Result()

    monkeypatch.setattr("subprocess.run", mock_run)

    try:
        # Test running the script
        result = run_script(script_path)
        assert result == 0
    finally:
        # Clean up
        os.unlink(script_path)
