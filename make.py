#!/usr/bin/python3
import os
import sys
from datetime import datetime
import subprocess

WORKDIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_REPO_PATH = "/var/cache/pacman/offline-repo"

def run_command(command):
    result = subprocess.run(command, shell=True, check=True)
    return result.returncode

def cleanup():
    try:
        if os.path.isdir(f"{WORKDIR}/bin"):
            run_command(f"rm -rf {WORKDIR}/bin/*")
        else:
            run_command(f"mkdir -p {WORKDIR}/bin")
        
        if not os.path.isdir(f"{WORKDIR}/builds"):
            run_command(f"mkdir -p {WORKDIR}/builds")
    except subprocess.CalledProcessError:
        print("Error during cleanup. Aborting.")
        sys.exit(1)

def build(offline: bool, refresh_offline_repo: bool = True):
    try:
        paths_to_remove = [
            "secux-apps",
            "secux-installer",
            "kirt-app"
        ]
        
        for path in paths_to_remove:
            full_path = f"{WORKDIR}/releng/airootfs/usr/local/share/{path}"
            if os.path.isdir(full_path):
                run_command(f"rm -rf {full_path}")
        
        run_command(f"mkdir -p {WORKDIR}/releng/airootfs/var/cache/pacman")
        
        repos = {
            "secux-installer": "https://github.com/kolbanidze/secux-installer.git",
            "secux-apps": "https://github.com/kolbanidze/secux-apps.git",
            "kirt-app": "https://github.com/kirt-king/test_app.git"
        }
        
        for repo, url in repos.items():
            run_command(f"git clone --depth=1 {url} {WORKDIR}/releng/airootfs/usr/local/share/{repo}")
            
        run_command(f"touch {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/production.conf")
        
        if offline:
            run_command(f"touch {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf")
            if refresh_offline_repo or not os.path.isdir(f"{WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo"):
                run_command(f"rm -rf {WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo")
                run_command(f"rsync -aAXHv --info=progress2 {OFFLINE_REPO_PATH} {WORKDIR}/releng/airootfs/var/cache/pacman/")
            run_command(f"cp {WORKDIR}/releng/airootfs/etc/pacman_offline.conf {WORKDIR}/releng/airootfs/etc/pacman.conf")
        else:
            run_command(f"cp {WORKDIR}/releng/airootfs/etc/pacman_online.conf {WORKDIR}/releng/airootfs/etc/pacman.conf")
            run_command(f"rm -rf {WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo/*")
            offline_conf = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf"
            if os.path.isfile(offline_conf):
                run_command(f"rm {offline_conf}")
        
        if offline:
            run_command(f"chmod +x {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/collect_python_packages.sh")
            run_command(f"bash {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/collect_python_packages.sh {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages")
        
        run_command(f"mkarchiso -v -w {WORKDIR}/bin -o {WORKDIR}/bin {WORKDIR}/releng")
        buildtype = "offline" if offline else "online"
        run_command(f"mv {WORKDIR}/bin/*.iso {WORKDIR}/builds/SecuxLinux-{buildtype}-{datetime.today().strftime('%Y-%m-%d_%H-%M')}.iso")
    except subprocess.CalledProcessError:
        print("Error during build process. Aborting.")
        sys.exit(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run as root!")
        sys.exit(1)
    
    cleanup()
    build(offline=False)
    cleanup()
    
    if os.path.isdir(OFFLINE_REPO_PATH):
        build(offline=True, refresh_offline_repo=True)
    else:
        print("ERROR. Offline repo wasn't found on device!")
        sys.exit(1)
    
    cleanup()
