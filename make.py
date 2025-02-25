#!/usr/bin/python3
import os
from datetime import datetime

WORKDIR = os.path.dirname(os.path.abspath(__file__))

OFFLINE_REPO_PATH = "/var/cache/pacman/offline-repo"

def cleanup():
    if os.path.isdir(f"{WORKDIR}/bin"):
        os.system(f"rm -rf {WORKDIR}/bin/*")
    else:
        os.system(f"mkdir -p {WORKDIR}/bin")
    
    if not os.path.isdir(f"{WORKDIR}/builds"):
        os.system(f"mkdir -p {WORKDIR}/builds")

def build(offline: bool, refresh_offline_repo: bool = True):
    if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-apps"):
        os.system("rm -rf {WORKDIR}/releng/airootfs/usr/local/share/secux-apps")
    if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer"):
        os.system("rm -rf {WORKDIR}/releng/airootfs/usr/local/share/secux-installer")
    if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/kirt-app"):
        os.system("rm -rf {WORKDIR}/releng/airootfs/usr/local/share/kirt-app")

    os.system(f"git clone --depth=1 https://github.com/kolbanidze/secux-installer.git {WORKDIR}/releng/airootfs/usr/local/share/secux-installer")
    os.system(f"git clone --depth=1 https://github.com/kolbanidze/secux-apps.git {WORKDIR}/releng/airootfs/usr/local/share/secux-apps")
    os.system(f"git clone --depth=1 https://github.com/kirt-king/test_app.git {WORKDIR}/releng/airootfs/usr/local/share/kirt-app")

    os.system(f"touch {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/production.conf")
    if offline:
        os.system(f"touch {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf")
        if refresh_offline_repo or not os.path.isdir(f"{WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo"):
            os.system(f"rm -rf {WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo")
            os.system(f"rsync -aAXHv --info=progress2 {OFFLINE_REPO_PATH} {WORKDIR}/releng/airootfs/var/cache/pacman/")
        os.system(f"cp {WORKDIR}/releng/airootfs/etc/pacman_offline.conf {WORKDIR}/releng/airootfs/etc/pacman.conf")
    else:
        os.system(f"cp {WORKDIR}/releng/airootfs/etc/pacman_online.conf {WORKDIR}/releng/airootfs/etc/pacman.conf")
        os.system(f"rm -rf {WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo/*")
        if os.path.isfile(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf"):
            os.system(f"rm {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf")

    if offline:
        os.system(f"./{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/collect_python_packages.sh {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages")
    
    os.system(f"mkarchiso -v -w {WORKDIR}/bin -o {WORKDIR}/bin {WORKDIR}/releng")
    buildtype = "offline" if offline else "online"
    os.system(f"mv {WORKDIR}/bin/*.iso {WORKDIR}/builds/SecuxLinux-{buildtype}-{datetime.today().strftime("%Y-%m-%d_%H-%M")}.iso")


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run as root!")
        exit(1)
    cleanup()
    build(offline=False)
    cleanup()
    if os.path.isdir(OFFLINE_REPO_PATH):
        build(offline=True, refresh_offline_repo=True)
    else:
        print("ERROR. Offline repo wasn't found on device!")
        exit(1)
    cleanup()
