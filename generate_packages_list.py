from subprocess import run

# Not required anymore. Secux Linux Builder automatically updates list of packages.
# Scheduled for removal.

def _get_metapackages(metapackage) -> list:
    cmd = run(['pacman', '-Sg', metapackage], check=True, capture_output=True)
    return [i.split(' ')[-1] for i in cmd.stdout.decode().strip().split("\n")]

# OS, Apps and dependencies
packages = ['base', 'base-devel', 'linux', 'linux-lts', 'linux-hardened', 'linux-headers', 'linux-lts-headers', 'linux-hardened-headers', 'linux-firmware', 'amd-ucode', 'intel-ucode', 'vim', 'nano', 'efibootmgr', 'sudo', 'plymouth', 'python-pip', 'python-dbus', 'v4l-utils', 'lvm2', 'networkmanager', 'systemd-ukify', 'sbsigntools', 'efitools', 'less', 'git', 'ntfs-3g', 'gvfs', 'gvfs-mtp', 'xdg-user-dirs', 'fwupd', 'sbctl', 'shim-signed', 'mokutil', 'networkmanager-openvpn', 'gnome-tweaks']

packages += ['vlc', 'firefox', 'chromium', 'libreoffice', 'keepassxc']

packages += ['tk', 'python-pexpect', 'python-pillow', 'python-opencv', 'python-numpy', 'python-sqlalchemy', 'python-psycopg2', 'python-darkdetect', 'python-packaging', 'python-setuptools', 'python-dotenv', 'python-dlib']

packages += ['libpam-google-authenticator', 'python-qrcode', 'vte4', 'apparmor', 'ufw']

packages += _get_metapackages('gnome')

packages += _get_metapackages('plasma')
packages += _get_metapackages('kde-applications')

packages += _get_metapackages('xorg')

# Getting all dependencies

dependencies = []

for package in packages:
    cmd = run(["pactree", '-su', package], capture_output=True, check=True)
    output = cmd.stdout.decode().strip().split('\n')
    dependencies.extend(output)
dependencies = list(set(dependencies))
dependencies.extend(["xorg", "gnome", "plasma"])

for i in range(len(dependencies)):
    if "<" in dependencies[i]: 
        dependencies[i] = dependencies[i].split("<")[0]
        continue
    if ">" in dependencies[i]:
        dependencies[i] = dependencies[i].split(">")[0]
        continue
    if "=" in dependencies[i]:
        dependencies[i] = dependencies[i].split("=")[0]

print(sorted(dependencies))
