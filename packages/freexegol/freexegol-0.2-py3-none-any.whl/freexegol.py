import sys
import os
import time
import docker
import subprocess
from pathlib import Path
from git import Repo


def start(container_name):
    client = docker.from_env()
    image_tag = f"freexegol"

    # check if container already exists
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
        return
    except docker.errors.NotFound:
        pass

    # create new container and folders
    home = Path.home()
    local_container = os.path.abspath(str(home) + "\\.freexegol\\" + container_name)
    if not os.path.isdir(local_container):
        os.makedirs(local_container, exist_ok=True)
    local_workspace = os.path.abspath(str(home) + "\\.freexegol\\" + container_name + "\\workspace")
    if not os.path.isdir(local_workspace):
        os.makedirs(local_workspace, exist_ok=True)

    # Run container with workspace
    print(f"[*] Starting container '{container_name}' from image '{image_tag}'...")
    container = client.containers.run(
        image_tag,
        name=container_name,
        hostname=container_name,
        command="/bin/zsh",
        detach=True,
        tty=True,
        stdin_open=True,
        remove=False,
        user=0,
        volumes={
            local_workspace: {'bind': '/workspace', 'mode': 'rw'}
        }
    )



def build():
    # retrieves dockerfile
    home = Path.home()
    dockerfile_path = os.path.abspath(str(home) + "\\.freexegol\\Freexegol\\image\\freexegol.dockerfile")
    if not os.path.isfile(dockerfile_path):
        print(f"[!] Error: Cannot find Dockerfile freexegol.dockerfile !")
        sys.exit(1)

    client = docker.from_env()
    image_tag = f"freexegol"

    # Build image
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




def main():
    # create main folder if not exists
    home = Path.home()
    Path(str(home) + "\\.freexegol").mkdir(parents=True, exist_ok=True)

    # check assets and retrieves it if not here
    check_assets = os.path.abspath(str(home) + "\\.freexegol\\Freexegol")
    if not os.path.isdir(check_assets):
        print("[+] Freexegol folders structure not exists. Trying to create it...")
        Repo.clone_from("https://github.com/processust/Freexegol", str(home) + "\\.freexegol\\")
    
    # TODO :
    #   "build" build local image to docker image
    #   "install" retrieves image from docker hub
    #   "start" start a container
    #   "stop" stop a container
    #   "inspect" ask docker for inspection
    #   "remove" completely destroy a container
    #   log with asciinema
        
    if len(sys.argv) == 2 and sys.argv[1] == "build":
        print(f"[+] Trying to build image...")
        build()
    elif len(sys.argv) == 2 and sys.argv[1] == "install":
        print(f"[+] Not implemented yet !")
        sys.exit(0)
    elif len(sys.argv) == 3 and sys.argv[1] == "start":
        print(f"[+] Trying to build {sys.argv[2]} container...")
        start(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "stop":
        print(f"[+] Not implemented yet !")
        sys.exit(0)
    elif len(sys.argv) == 3 and sys.argv[1] == "inspect":
        print(f"[+] Not implemented yet !")
        sys.exit(0)
    elif len(sys.argv) == 3 and sys.argv[1] == "remove":
        print(f"[+] Not implemented yet !")
        sys.exit(0)
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
\tfreexegol start <container_name>
\tfreexegol stop <container_name>
\tfreexegol inspect <container_name>
\tfreexegol remove <container_name>

        '''
        print(help_string)
        sys.exit(0)
    

if __name__ == "__main__":
    main()
