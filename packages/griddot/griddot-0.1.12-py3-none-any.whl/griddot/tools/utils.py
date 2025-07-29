import subprocess

def get_container_command():
    """
    Check if Podman is installed, if not, use Docker.
    Returns the command to use for container operations.
    """
    container_cmd = "podman"
    try:
        subprocess.run("podman --version", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Podman is not installed. Using Docker instead.")
        container_cmd = "docker"
    return container_cmd
