#!/usr/bin/env bash

iso_name="Secux"
iso_label="$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y-%m-%d_%H-%M)"
iso_publisher="Secux Linux https://github.com/kolbanidze/secux-iso"
iso_application="Secux Linux Live/Rescue DVD"
#iso_version="$(date +"%Y-%m-%d_%H-%M")"
iso_version="Linux"
install_dir="secuxdir"
buildmodes=('iso')
bootmodes=('bios.syslinux' 'bios.syslinux'
           'uefi.systemd-boot')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M' '-Xdict-size' '1M')
bootstrap_tarball_compression=('zstd' '-c' '-T0' '--auto-threads=logical' '--long' '-19')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/usr/local/share/secux-installer"]="0:0:755"
  ["/root"]="0:0:750"
  ["/root/.automated_script.sh"]="0:0:755"
  ["/root/.gnupg"]="0:0:700"
  ["/usr/local/bin/choose-mirror"]="0:0:755"
  ["/usr/local/bin/Installation_guide"]="0:0:755"
  ["/usr/local/bin/livecd-sound"]="0:0:755"
)
