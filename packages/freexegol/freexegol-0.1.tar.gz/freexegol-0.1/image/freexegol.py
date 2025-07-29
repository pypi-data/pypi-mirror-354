import sys
import os
import docker
import subprocess

def build_and_run(container_name):
    dockerfile_path = os.path.abspath("freexegol.dockerfile")
    if not os.path.isfile(dockerfile_path):
        print(f"Error: Cannot find Dockerfile freexegol.dockerfile in current directory.")
        sys.exit(1)
    
    # Répertoire local à partager
    local_workspace = os.path.abspath("workspace")
    if not os.path.isdir(local_workspace):
        print(f"[*] Creating local 'workspace' directory at {local_workspace}")
        os.makedirs(local_workspace, exist_ok=True)

    client = docker.from_env()
    image_tag = f"freexegol_{container_name}"

    # Vérifie si le conteneur existe déjà
    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            print(f"[*] Container '{container_name}' exists but is not running. Starting it...")
            container.start()
            print(f"[+] Container '{container_name}' started (id: {container.short_id}).")
        else:
            print(f"[!] Container '{container_name}' already running (id: {container.short_id}).")
        
        print(f"[~] Opening interactive shell in '{container_name}'...\n")
        subprocess.call(["docker", "exec", "-it", container_name, "/bin/zsh"])
        print("\n[!] Shell closed. (Container is always running in background unless you configured an auto-stop policy)")
        return
    except docker.errors.NotFound:
        pass
    
    # Build image
    print(f"[*] Building image from '{dockerfile_path}' with tag '{image_tag}'...")
    image, build_logs = client.images.build(
        path=os.path.dirname(dockerfile_path),
        dockerfile=os.path.basename(dockerfile_path),
        tag=image_tag,
        rm=True
    )
    for chunk in build_logs:
        if 'stream' in chunk:
            line = chunk['stream'].strip()
            if line:
                print(line)

    print(f"[+] Image '{image_tag}' built.")

    # Run container en montant le volume
    print(f"[*] Starting container '{container_name}' from image '{image_tag}'...")
    container = client.containers.run(
        image_tag,
        name=container_name,
        command="/bin/zsh",
        detach=True,
        tty=True,
        stdin_open=True,
        volumes={
            local_workspace: {'bind': '/workspace', 'mode': 'rw'}
        }
    )
    print(f"[+] Container '{container.name}' started (id: {container.short_id}).")
    print(f"[+] Local directory '{local_workspace}' mounted as '/workspace' in container.")
    
    print(f"[~] Opening interactive shell in '{container_name}'...\n")
    try:
        subprocess.call(["docker", "logs", "-f", container_name])
    except KeyboardInterrupt:
        pass

    print("\n[!] Shell closed. (Container is always running in background unless you configured an auto-stop policy)")


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "start":
        print("Usage: freexegol start <container_name>")
        sys.exit(1)
    
    container_name = sys.argv[2]
    build_and_run(container_name)

if __name__ == "__main__":
    main()
