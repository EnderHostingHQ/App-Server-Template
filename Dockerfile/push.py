from result import Ok, Err, Result, is_ok, is_err
import subprocess
from typing import List, Tuple

from utils import discover_builds

def main():
    push_all()

def push(name: str, tag: str) -> Result[str, str]:
    """
    Push a Docker image with the specified name and tag to Docker Hub.
ch
    Args:
        name: The name of the image
        tag: The tag of the image

    Returns:
        Result[str, str]: Ok with success message or Err with error message
    """
    try:
        image_name = f"enderhostinghq/{name}:{tag}"

        cmd = ["docker", "push", image_name]

        print(f"Pushing Docker image: {image_name}")
        print(f"Command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        return Ok(f"Docker image '{image_name}' pushed successfully")

    except subprocess.CalledProcessError as e:
        error_msg = f"Docker push failed: {e.stderr if e.stderr else e.stdout}"
        return Err(error_msg)
    except Exception as e:
        return Err(f"Unexpected error: {str(e)}")

def push_all(builds: List[Tuple[str, str]] = discover_builds()) -> None:
    """
    Push all available Docker images by auto-discovering available configurations.
    """

    if not builds:
        print("No build configurations found!")
        return

    print(f"Found {len(builds)} build configurations:")
    for name, tag in builds:
        print(f"  - {name}:{tag}")

    print("\nStarting pushes...\n")

    success_count = 0
    for name, tag in builds:
        print(f"--- Pushing {name}:{tag} ---")
        result = push(name, tag)

        if is_ok(result):
            print(f"✅ {result.unwrap()}")
            success_count += 1
        else:
            print(f"❌ {result.unwrap_err()}")
        print()

    print(f"Push complete: {success_count}/{len(builds)} succeeded")

if __name__ == "__main__":
    main()
