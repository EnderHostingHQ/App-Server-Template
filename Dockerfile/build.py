from result import Ok, Err, Result, is_ok, is_err
import subprocess
import os
from typing import List, Tuple

from utils import discover_builds

def main():
    build_all()

def build(name: str, tag: str) -> Result[str, str]:
    """
    Build a Docker image with the specified name and tag.

    Args:
        name: The name of the image
        tag: The tag of the image

    Returns:
        Result[str, str]: Ok with success message or Err with error message
    """
    try:
        image_name = f"enderhostinghq/{name}:{tag}"

        context_path = f"./{name}/{tag}"

        if not os.path.exists(context_path):
            return Err(f"Build context path '{context_path}' does not exist")

        cmd = ["docker", "build", "-t", image_name, context_path]

        print(f"Building Docker image: {image_name}")
        print(f"Build context: {context_path}")
        print(f"Command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        return Ok(f"Docker image '{image_name}' built successfully")

    except subprocess.CalledProcessError as e:
        error_msg = f"Docker build failed: {e.stderr if e.stderr else e.stdout}"
        return Err(error_msg)
    except Exception as e:
        return Err(f"Unexpected error: {str(e)}")

def build_all(builds: List[Tuple[str, str]] = discover_builds()) -> None:
    """
    Build all available Docker images by auto-discovering available configurations.
    """

    if not builds:
        print("No build configurations found!")
        return

    print(f"Found {len(builds)} build configurations:")
    for name, tag in builds:
        print(f"  - {name}:{tag}")

    print("\nStarting builds...\n")

    success_count = 0
    for name, tag in builds:
        print(f"--- Building {name}:{tag} ---")
        result = build(name, tag)

        if is_ok(result):
            print(f"✅ {result.unwrap()}")
            success_count += 1
        else:
            print(f"❌ {result.unwrap_err()}")
        print()

    print(f"Build complete: {success_count}/{len(builds)} succeeded")

if __name__ == "__main__":
    main()
