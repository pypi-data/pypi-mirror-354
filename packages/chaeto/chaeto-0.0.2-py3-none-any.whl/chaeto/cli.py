"""Simple CLI for chaeto project."""
import os
import re
import subprocess
import tempfile

import fire
from loguru import logger


def parse_script_requirements(script_path: str) -> tuple[str | None, list[str]]:
    """Parse Python version and dependencies from script comments.

    Looks for a special comment block in the format:
    # /// script
    # requires-python = ">=3.12"
    # dependencies = [
    #     "package1==1.0.0",
    #     "package2>=2.0.0",
    # ]
    # ///

    Args:
        script_path: Path to the Python script

    Returns:
        Tuple of (python_version_constraint, dependencies)

    """
    python_version_constraint = None
    dependencies = []

    with open(script_path) as f:
        content = f.read()

    # Extract the script block if it exists
    script_block_match = re.search(r"# /// script\n(.*?)# ///", content, re.DOTALL)
    if not script_block_match:
        return python_version_constraint, dependencies

    script_block = script_block_match.group(1)

    # Extract Python version
    python_version_match = re.search(r'# requires-python = "(.*?)"', script_block)
    if python_version_match:
        python_version_constraint = python_version_match.group(1)

    # Extract dependencies
    deps_match = re.search(r"# dependencies = \[(.*?)\]", script_block, re.DOTALL)
    if deps_match:
        deps_block = deps_match.group(1)
        # Extract each dependency
        for line in deps_block.split("\n"):
            dep_match = re.search(r'#\s*"(.*?)"', line)
            if dep_match:
                dependencies.append(dep_match.group(1))

    return python_version_constraint, dependencies


def extract_python_version(version_constraint: str) -> str:
    """Extract a specific Python version from a version constraint.

    Args:
        version_constraint: A PEP 440 version constraint like ">=3.12"

    Returns:
        A specific Python version like "3.12"

    """
    # Extract the version number from constraints like >=3.12, ==3.12, etc.
    match = re.search(r'(\d+\.\d+)', version_constraint)
    if match:
        return match.group(1)
    return "3.12"  # Default to Python 3.12 if we can't parse the constraint


def run_script(script_path: str, cleanup: bool = True) -> int:
    """Execute a Python script in a virtual environment created on the fly.

    Args:
        script_path: Path to the Python script to execute
        cleanup: Whether to clean up the temporary virtual environment after execution

    Returns:
        Exit code from the script execution

    """
    script_path = os.path.abspath(script_path)
    if not os.path.exists(script_path):
        logger.error(f"Script not found: {script_path}")
        return 1

    # Parse script requirements
    python_version_constraint, dependencies = parse_script_requirements(script_path)

    # Create a temporary directory for the virtual environment
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = os.path.join(temp_dir, "venv")
        logger.info(f"Creating virtual environment in {venv_path}")

        # Extract a specific Python version from the constraint
        python_version = None
        if python_version_constraint:
            python_version = extract_python_version(python_version_constraint)
            logger.info(f"Using Python {python_version} (from constraint {python_version_constraint})")

        # Create virtual environment with the specified Python version or default to system Python
        try:
            cmd = ["uv", "venv", venv_path]
            if python_version:
                cmd.extend(["--python", python_version])

            subprocess.run(
                cmd,
                shell=False,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create virtual environment: {e}")
            logger.error(f"stdout: {e.stdout.decode()}")
            logger.error(f"stderr: {e.stderr.decode()}")
            return 1

        # Install dependencies if any
        if dependencies:
            logger.info(f"Installing dependencies: {' '.join(dependencies)}")
            try:
                cmd = ["uv", "pip", "install", "--python", f"{venv_path}/bin/python"]
                cmd.extend(dependencies)

                subprocess.run(
                    cmd,
                    shell=False,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install dependencies: {e}")
                logger.error(f"stdout: {e.stdout.decode()}")
                logger.error(f"stderr: {e.stderr.decode()}")
                return 1

        # Execute the script
        logger.info(f"Executing script: {script_path}")
        try:
            python_executable = os.path.join(venv_path, "bin", "python")
            result = subprocess.run(
                [python_executable, script_path],
                shell=False,
                check=False,
            )
            return result.returncode
        except Exception as e:
            logger.error(f"Failed to execute script: {e}")
            return 1


def main():
    """Entry point for the CLI."""
    fire.Fire({"run": run_script})


if __name__ == "__main__":
    main()
