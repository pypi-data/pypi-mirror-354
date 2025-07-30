import sys
import os
import datetime
import shutil
import time
import json
import docker
import subprocess
from pathlib import Path
from git import Repo


def info():
    client = docker.from_env()
    containers = client.containers.list(all=True)
    print("Conteneurs Docker :")
    for container in containers:
        print(f"ID : {container.short_id}")
        print(f"Nom : {container.name}")
        print(f"Image : {container.image.tags[0] if container.image.tags else 'N/A'}")
        print(f"Statut : {container.status}")
        print("-" * 30)
    images = client.images.list()
    print("\nImages Docker :")
    for image in images:
        print(f"ID : {image.short_id}")
        print(f"Tags : {', '.join(image.tags) if image.tags else 'Aucun tag'}")
        print(f"Taille : {image.attrs['Size'] / (1024 * 1024):.2f} MB")
        print("-" * 30)


def get_docker_wsl_distribution():
    try:
        result = subprocess.run(
            ['wsl.exe', '-l', '-v'],
            capture_output=True,
            encoding='utf-16le'   # !! c'est la clé !
        )

        output = result.stdout
        for line in output.splitlines():
            line = line.strip()
            if not line or "NAME" in line:
                continue
            parts = line.split()
            if parts[0] == "*":
                parts = parts[1:]
            if len(parts) >= 3:
                name = parts[0]
                state = parts[1]
                version = parts[2]
                if state == 'Running' and version == '2':
                    if name not in ['docker-desktop', 'docker-desktop-data']:
                        return name
        return None
    except subprocess.CalledProcessError as e:
        print(f"[!] Erreur lors de la récupération de la machine WSL2 : {e}")
        return None


def record_session(container_name):
    home = Path.home()
    container_dir = os.path.abspath(str(home) + "\\.freexegol\\" + container_name)
    if not os.path.isdir(container_dir):
        print(f"[!] Folder '{container_dir}' does not exist.")
        sys.exit(1)
    logdir = str(container_dir) + "\\workspace\\logs"
    if not os.path.isdir(logdir):
        os.makedirs(logdir, exist_ok=True)
    old_session = str(logdir) + "\\session.asciinema"
    if os.path.exists(old_session):
        print(f"[*] Old session exists in '{container_dir}' !")
        os.remove(old_session)
        print(f"[+] Old session deleted.")
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        print(f"[+] Starting asciinema recording in container '{container_name}'...")
    except docker.errors.NotFound:
        print(f"[!] Container '{container_name}' does not exist.")
        sys.exit(1)
    except docker.errors.APIError as e:
        print(f"[!] Failed to remove container '{container_name}': {e}")
        sys.exit(1)
    cmd_in_container = (
        f"asciinema rec -i 2 --stdin --quiet "
        f'--command "/bin/zsh" '
        f'--title "$(hostname | sed \'s/^freexegol-/[FREEXEGOL] /\') $(date \'+%d/%m/%Y %H:%M:%S\')" '
        f"/workspace/logs/session.asciinema"
    )
    try:
        subprocess.call([
            "docker", "exec", "-it", "-w", "/root", container_name, 
            "sh", "-c", cmd_in_container
        ])
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filelog = os.path.join(logdir, f"{container_name}_{timestamp}.asciinema")
        os.rename(old_session, filelog)
        print(f"[+] Recording saved to {filelog}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during session recording: {e}")




def inspect(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        details = container.attrs  # Low-level API details (dict)
        info = {
            "ID": details.get("Id"),
            "Name": details.get("Name", "").lstrip("/"),
            "Image": details.get("Config", {}).get("Image"),
            "Created": details.get("Created"),
            "Status": details.get("State", {}).get("Status"),
            "Running": details.get("State", {}).get("Running"),
            "StartedAt": details.get("State", {}).get("StartedAt"),
            "FinishedAt": details.get("State", {}).get("FinishedAt"),
            "RestartCount": details.get("RestartCount"),
            "Ports": details.get("NetworkSettings", {}).get("Ports"),
            "Mounts": [
                f"{mnt.get('Source')}:{mnt.get('Destination')}"
                for mnt in details.get("Mounts", [])
            ],
            "Env": details.get("Config", {}).get("Env"),
            "Entrypoint": details.get("Config", {}).get("Entrypoint"),
            "Cmd": details.get("Config", {}).get("Cmd"),
            "Networks": list(details.get("NetworkSettings", {}).get("Networks", {}).keys()),
            "Labels": details.get("Config", {}).get("Labels"),
            "HostConfig": details.get("HostConfig", {}),
        }
        print(json.dumps(info, indent=2))
    except docker.errors.NotFound:
        print(f"[!] Container '{container_name}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error inspecting container: {e}")
        sys.exit(1)


def remove(container_name):
    import docker
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        print(f"[*] Removing container '{container_name}' (id: {container.short_id})...")
        if container.status == "running":
            print(f"[~] Container is running, stopping it first...")
            container.stop()
        container.remove()
        print(f"[+] Container '{container_name}' has been removed.")
    except docker.errors.NotFound:
        print(f"[!] Container '{container_name}' does not exist.")
        sys.exit(1)
    except docker.errors.APIError as e:
        print(f"[!] Failed to remove container '{container_name}': {e}")
        sys.exit(1)
    home = Path.home()
    shared_dir = os.path.abspath(str(home) + "\\.freexegol\\" + container_name)
    if os.path.exists(shared_dir):
        confirm = input(
            f"[?] Do you want to DELETE the local shared folder '{shared_dir}' and all its contents? (y/N): "
        ).strip().lower()
        if confirm == "y" or confirm == "yes":
            try:
                shutil.rmtree(shared_dir)
                print(f"[+] Directory '{shared_dir}' deleted.")
            except Exception as e:
                print(f"[!] Error while deleting the directory: {e}")
                sys.exit(1)
        else:
            print(f"[-] Directory was kept.")
            sys.exit(0)
    else:
        print(f"[!] Shared directory '{shared_dir}' not found.")
        sys.exit(1)




def stop(container_name):
    import docker
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        if container.status == "running":
            print(f"[*] Stopping running container '{container_name}' (id: {container.short_id})...")
            container.stop()
            print(f"[+] Container '{container_name}' stopped.")
            sys.exit(0)
        else:
            print(f"[!] Container '{container_name}' is not running (status: {container.status}).")
            sys.exit(1)
    except docker.errors.NotFound:
        print(f"[!] Container '{container_name}' does not exist.")
        sys.exit(1)




def init(container_name):
    client = docker.from_env()
    image_tag = f"freexegol"
    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            print(f"[*] Container '{container_name}' exists but is not running. Starting it...")
            container.start()
            print(f"[+] Container '{container_name}' started (id: {container.short_id}).")
        else:
            print(f"[!] Container '{container_name}' already running (id: {container.short_id}).")
        print(f"[~] Opening interactive shell in '{container_name}'...\n")
        subprocess.call(["docker", "logs", "-f", container_name])
        return
    except docker.errors.NotFound:
        pass
    home = Path.home()
    local_container = os.path.abspath(str(home) + "\\.freexegol\\" + container_name)
    if not os.path.isdir(local_container):
        os.makedirs(local_container, exist_ok=True)
    local_workspace = os.path.abspath(str(home) + "\\.freexegol\\" + container_name + "\\workspace")
    if not os.path.isdir(local_workspace):
        os.makedirs(local_workspace, exist_ok=True)
    docker_wsl_distro = get_docker_wsl_distribution()
    print(f"[*] Starting container '{container_name}' from image '{image_tag}'...")
    container = client.containers.run(
        image_tag,
        name=container_name,
        hostname=container_name,
        command="/entrypoint.sh",
        detach=True,
        tty=True,
        stdin_open=True,
        remove=False,
        user=0,
        environment={
            'DISPLAY': os.environ.get('DISPLAY', ':0'),  
            'LIBGL_ALWAYS_INDIRECT': '0'
        },
        volumes={
            "\\\\wsl.localhost\\" + str(docker_wsl_distro) + "\\mnt\\wslg\\.X11-unix": {"bind": "/tmp/.X11-unix", "mode": "rw"},
            local_workspace: {'bind': '/workspace', 'mode': 'rw'}
        }
    )
    subprocess.call(["docker", "logs", "-f", container_name])





def start(container_name):
    client = docker.from_env()
    image_tag = f"freexegol"
    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            print(f"[*] Container '{container_name}' exists but is not running. Starting it...")
            container.start()
            print(f"[+] Container '{container_name}' started (id: {container.short_id}).")
        else:
            print(f"[!] Container '{container_name}' already running (id: {container.short_id}).")
        print(f"[~] Opening interactive shell in '{container_name}'...\n")
        subprocess.call(["docker", "exec", "-it", "-w", "/root", container_name, "/bin/zsh"])
        return
    except docker.errors.NotFound:
        pass
    home = Path.home()
    local_container = os.path.abspath(str(home) + "\\.freexegol\\" + container_name)
    if not os.path.isdir(local_container):
        os.makedirs(local_container, exist_ok=True)
    local_workspace = os.path.abspath(str(home) + "\\.freexegol\\" + container_name + "\\workspace")
    if not os.path.isdir(local_workspace):
        os.makedirs(local_workspace, exist_ok=True)
    docker_wsl_distro = get_docker_wsl_distribution()
    print(f"[*] Starting container '{container_name}' from image '{image_tag}'...")
    container = client.containers.run(
        image_tag,
        name=container_name,
        hostname=container_name,
        command="/entrypoint.sh",
        detach=True,
        tty=True,
        stdin_open=True,
        remove=False,
        user=0,
        environment={
            'DISPLAY': os.environ.get('DISPLAY', ':0'),  
            'LIBGL_ALWAYS_INDIRECT': '0'
        },
        volumes={
            "\\\\wsl.localhost\\" + str(docker_wsl_distro) + "\\mnt\\wslg\\.X11-unix": {"bind": "/tmp/.X11-unix", "mode": "rw"},
            local_workspace: {'bind': '/workspace', 'mode': 'rw'}
        }
    )



def build():
    home = Path.home()
    dockerfile_path = os.path.abspath(str(home) + "\\.freexegol\\Freexegol\\image\\freexegol.dockerfile")
    if not os.path.isfile(dockerfile_path):
        print(f"[!] Error: Cannot find Dockerfile freexegol.dockerfile !")
        sys.exit(1)
    client = docker.from_env()
    image_tag = f"freexegol"
    print(f"[*] Building image from '{dockerfile_path}'...")
    image, build_logs = client.images.build(
        path=os.path.dirname(dockerfile_path),
        dockerfile=os.path.basename(dockerfile_path),
        tag=image_tag,
        nocache=True,
        rm=True
    )
    for chunk in build_logs:
        if 'stream' in chunk:
            line = chunk['stream'].strip()
            if line:
                print(line)
    print(f"[+] Image '{image_tag}' built.")
    print(f"[+] You can initialize a new container now : freexegol init <container_name>")





def main():
    home = Path.home()
    Path(str(home) + "\\.freexegol").mkdir(parents=True, exist_ok=True)
    check_assets = os.path.abspath(str(home) + "\\.freexegol\\Freexegol")
    if not os.path.isdir(check_assets):
        print("[+] Freexegol folders structure not exists. Trying to create it...")
        Repo.clone_from("https://github.com/processust/Freexegol", str(home) + "\\.freexegol\\Freexegol\\")
    
    # TODO :
    #   "install" retrieves image from docker hub
    if len(sys.argv) == 2 and sys.argv[1] == "build":
        print(f"[+] Trying to build image...")
        build()
    elif len(sys.argv) == 2 and (sys.argv[1] == "info" or sys.argv[1] == "infos"):
        info()
    elif len(sys.argv) == 2 and sys.argv[1] == "install":
        print(f"[+] Not implemented yet !")
        sys.exit(0)
    elif len(sys.argv) == 3 and sys.argv[1] == "start":
        print(f"[+] Trying to start {sys.argv[2]} container...")
        start(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "init":
        print(f"[+] Trying to initialize {sys.argv[2]} container...")
        init(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "record":
        print(f"[+] Trying to record {sys.argv[2]} container...")
        record_session(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "stop":
        print(f"[+] Trying to stop {sys.argv[2]} container...")
        stop(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "inspect":
        print(f"[+] Trying to inspect {sys.argv[2]} container...")
        inspect(sys.argv[2])
    elif len(sys.argv) == 3 and (sys.argv[1] == "remove" or sys.argv[1] == "delete"):
        print(f"[+] Trying to remove {sys.argv[2]} container...")
        remove(sys.argv[2])
    else:
        help_string = '''
##############################################################################

                        FREEXEGOL PYTHON WRAPPER

   The free, open-source, and lifetime alternative to the Exegol project

    (actually, it's a crappy project but it's free for commercial use !)

##############################################################################

Usage :
\tfreexegol build
\tfreexegol install
\tfreexegol init <container_name>
\tfreexegol start <container_name>
\tfreexegol stop <container_name>
\tfreexegol inspect <container_name>
\tfreexegol remove <container_name>

        '''
        print(help_string)
        sys.exit(0)
    

if __name__ == "__main__":
    main()
