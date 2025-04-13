import os
import io
import subprocess
import threading
import queue
import shlex
import sys
import traceback
from argparse import ArgumentParser, BooleanOptionalAction
from typing import Any, Optional, List, Dict, Tuple, Union, Callable
from collections.abc import Callable
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from locale import getlocale
# Assuming language.py contains the Locale class as provided before
# from language import Locale
from pathlib import Path
from shutil import rmtree, copy, move
from language import Locale

VERSION = "3.0 ALPHA"
WORKDIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_REPO_PATH = "/var/cache/pacman/offline-repo" # Standard cache location
PACKAGES = ['a52dec', 'aalib', 'abseil-cpp', 'accessibility-inspector', 'accounts-qml-module', 'accountsservice', 'acl', 'adwaita-cursors', 'adwaita-fonts', 'adwaita-icon-theme', 'adwaita-icon-theme-legacy', 'aha', 'akonadi', 'akonadi-calendar', 'akonadi-calendar-tools', 'akonadi-contacts', 'akonadi-import-wizard', 'akonadi-mime', 'akonadi-search', 'akonadiconsole', 'akregator', 'alligator', 'alsa-card-profiles', 'alsa-lib', 'alsa-topology-conf', 'alsa-ucm-conf', 'amd-ucode', 'analitza', 'angelfish', 'aom', 'apache', 'apparmor', 'appstream', 'appstream-qt', 'apr', 'apr-util', 'archlinux-appstream-data', 'archlinux-keyring', 'argon2', 'arianna', 'aribb24', 'ark', 'artikulate', 'at-spi2-core', 'attica', 'attica5', 'attr', 'audex', 'audiocd-kio', 'audiofile', 'audiotube', 'audit', 'autoconf', 'automake', 'avahi', 'avogadro-crystals', 'avogadro-fragments', 'avogadro-molecules', 'avogadrolibs', 'avogadrolibs-qt5', 'awk', 'baloo', 'baloo-widgets', 'baobab', 'base', 'base-devel', 'bash', 'binutils', 'binutils', 'bison', 'black-hole-solver', 'blas', 'blinken', 'bluedevil', 'bluez', 'bluez-libs', 'bluez-qt', 'bolt', 'bomber', 'boost-libs', 'botan', 'bovo', 'breeze', 'breeze-gtk', 'breeze-icons', 'breeze-plymouth', 'brltty', 'brotli', 'bubblewrap', 'bzip2', 'ca-certificates', 'ca-certificates-mozilla', 'ca-certificates-utils', 'cairo', 'cairomm-1.16', 'calendarsupport', 'calligra', 'cantarell-fonts', 'cantor', 'cauchy', 'cblas', 'cdparanoia', 'cervisia', 'cfitsio', 'chromaprint', 'chromium', 'cifs-utils', 'clang', 'clinfo', 'clucene', 'cmark', 'colord', 'colord', 'colord-gtk-common', 'colord-gtk4', 'colord-kde', 'colord-sane', 'compiler-rt', 'composefs', 'confuse', 'convertlit', 'coordgen', 'coreutils', 'cracklib', 'cron', 'cryptsetup', 'cups-pk-helper', 'curl', 'curl', 'dav1d', 'db5.3', 'dbus', 'dbus-broker', 'dbus-broker-units', 'dbus-units', 'dconf', 'ddcutil', 'debugedit', 'decibels', 'default-cursors', 'desktop-file-utils', 'device-mapper', 'device-mapper', 'diffutils', 'discount', 'discover', 'djvulibre', 'dmidecode', 'docbook-xml', 'docbook-xsl', 'dolphin', 'dolphin-plugins', 'dotconf', 'double-conversion', 'dragon', 'drkonqi', 'duktape', 'e2fsprogs', 'ebook-tools', 'editorconfig-core-c', 'efibootmgr', 'efitools', 'efivar', 'egl-wayland', 'eglexternalplatform', 'elisa', 'emoji-font', 'enchant', 'epiphany', 'eventviews', 'evince', 'evolution-data-server', 'exempi', 'exiv2', 'expat', 'faac', 'faad2', 'fakeroot', 'falkon', 'ffmpeg', 'ffmpeg4.4', 'ffmpegthumbs', 'fftw', 'file', 'filelight', 'filesystem', 'findutils', 'firefox', 'flac', 'flashrom', 'flatpak', 'flatpak-kcm', 'flex', 'fluidsynth', 'fmt', 'folks', 'fontconfig', 'frameworkintegration', 'francis', 'freecell-solver', 'freeglut', 'freerdp', 'freerdp2', 'freetype2', 'frei0r-plugins', 'fribidi', 'fuse-common', 'fuse2', 'fuse3', 'futuresql', 'fwupd', 'fwupd-efi', 'gawk', 'gc', 'gcc', 'gcc-libs', 'gcr', 'gcr-4', 'gd', 'gdb', 'gdb-common', 'gdbm', 'gdbm', 'gdk-pixbuf2', 'gdm', 'geoclue', 'geocode-glib-2', 'geocode-glib-common', 'gettext', 'ghostscript', 'ghostwriter', 'giflib', 'git', 'gjs', 'glew', 'glib-networking', 'glib2', 'glibc', 'glibc', 'glibmm-2.68', 'glslang', 'glu', 'glycin', 'gmp', 'gnome', 'gnome-app-list', 'gnome-autoar', 'gnome-backgrounds', 'gnome-bluetooth-3.0', 'gnome-calculator', 'gnome-calendar', 'gnome-characters', 'gnome-clocks', 'gnome-color-manager', 'gnome-connections', 'gnome-console', 'gnome-contacts', 'gnome-control-center', 'gnome-desktop', 'gnome-desktop-4', 'gnome-desktop-common', 'gnome-disk-utility', 'gnome-font-viewer', 'gnome-keybindings', 'gnome-keyring', 'gnome-logs', 'gnome-maps', 'gnome-menus', 'gnome-mimeapps', 'gnome-music', 'gnome-online-accounts', 'gnome-remote-desktop', 'gnome-session', 'gnome-settings-daemon', 'gnome-shell', 'gnome-shell-extensions', 'gnome-software', 'gnome-system-monitor', 'gnome-text-editor', 'gnome-tour', 'gnome-tweaks', 'gnome-user-docs', 'gnome-user-share', 'gnome-weather', 'gnugo', 'gnulib-l10n', 'gnupg', 'gnupg', 'gnutls', 'gobject-introspection-runtime', 'gom', 'gperftools', 'gpgme', 'gpm', 'granatier', 'grantlee', 'grantlee-editor', 'grantleetheme', 'graphene', 'graphite', 'graphviz', 'grep', 'grilo', 'grilo-plugins', 'groff', 'gsettings-desktop-schemas', 'gsettings-system-schemas', 'gsettings-system-schemas', 'gsfonts', 'gsl', 'gsm', 'gsound', 'gspell', 'gssdp', 'gst-devtools-libs', 'gst-editing-services', 'gst-plugin-gtk', 'gst-plugin-gtk4', 'gst-plugin-pipewire', 'gst-plugins-bad', 'gst-plugins-bad-libs', 'gst-plugins-bad-libs', 'gst-plugins-base', 'gst-plugins-base-libs', 'gst-plugins-base-libs', 'gst-plugins-good', 'gst-python', 'gstreamer', 'gstreamer', 'gtest', 'gtk-update-icon-cache', 'gtk-vnc', 'gtk3', 'gtk4', 'gtkmm-4.0', 'gtksourceview4', 'gtksourceview5', 'gts', 'guile', 'gupnp', 'gupnp-av', 'gupnp-dlna', 'gupnp-igd', 'gvfs', 'gvfs', 'gvfs-afc', 'gvfs-dnssd', 'gvfs-goa', 'gvfs-goa', 'gvfs-google', 'gvfs-gphoto2', 'gvfs-mtp', 'gvfs-nfs', 'gvfs-onedrive', 'gvfs-smb', 'gvfs-wsdd', 'gwenview', 'gzip', 'harfbuzz', 'harfbuzz-icu', 'hdf5', 'hicolor-icon-theme', 'hidapi', 'highway', 'hunspell', 'hunspell', 'hwdata', 'hwloc', 'hyphen', 'i2c-tools', 'iana-etc', 'icu', 'id3lib', 'iio-sensor-proxy', 'ijs', 'imagemagick', 'imath', 'imlib2', 'incidenceeditor', 'initramfs', 'intel-ucode', 'iproute2', 'iptables', 'iputils', 'iso-codes', 'isoimagewriter', 'itinerary', 'jack', 'jansson', 'jasper', 'jbig2dec', 'jbigkit', 'jemalloc', 'js128', 'json-c', 'json-glib', 'jsoncpp', 'juk', 'k3b', 'kaccounts-integration', 'kaccounts-providers', 'kactivitymanagerd', 'kaddressbook', 'kajongg', 'kalarm', 'kalgebra', 'kalk', 'kalm', 'kalzium', 'kamera', 'kamoso', 'kanagram', 'kapman', 'kapptemplate', 'karchive', 'karchive5', 'kasts', 'kate', 'katomic', 'kauth', 'kauth5', 'kbackup', 'kbd', 'kblackbox', 'kblocks', 'kbookmarks', 'kbookmarks5', 'kbounce', 'kbreakout', 'kbruch', 'kcachegrind', 'kcachegrind-common', 'kcalc', 'kcalendarcore', 'kcalutils', 'kcharselect', 'kclock', 'kcmutils', 'kcmutils5', 'kcodecs', 'kcodecs5', 'kcolorchooser', 'kcolorpicker', 'kcolorscheme', 'kcompletion', 'kcompletion5', 'kconfig', 'kconfig5', 'kconfigwidgets', 'kconfigwidgets5', 'kcontacts', 'kcoreaddons', 'kcoreaddons5', 'kcrash', 'kcrash5', 'kcron', 'kdav', 'kdbusaddons', 'kdbusaddons5', 'kde-cli-tools', 'kde-dev-scripts', 'kde-dev-utils', 'kde-gtk-config', 'kde-inotify-survey', 'kdebugsettings', 'kdeclarative', 'kdeclarative5', 'kdeconnect', 'kdecoration', 'kded', 'kded5', 'kdeedu-data', 'kdegraphics-mobipocket', 'kdegraphics-thumbnailers', 'kdenetwork-filesharing', 'kdenlive', 'kdepim-addons', 'kdepim-runtime', 'kdeplasma-addons', 'kdesdk-kio', 'kdesdk-thumbnailers', 'kdesu', 'kdesu5', 'kdevelop', 'kdevelop-php', 'kdevelop-python', 'kdf', 'kdiagram', 'kdialog', 'kdiamond', 'kdnssd', 'kdoctools', 'kdsoap-qt6', 'kdsoap-ws-discovery-client', 'keditbookmarks', 'keepassxc', 'keysmith', 'keyutils', 'kfilemetadata', 'kfind', 'kfourinline', 'kgamma', 'kgeography', 'kget', 'kglobalaccel', 'kglobalaccel5', 'kglobalacceld', 'kgoldrunner', 'kgpg', 'kgraphviewer', 'kguiaddons', 'kguiaddons5', 'khangman', 'khealthcertificate', 'khelpcenter', 'kholidays', 'ki18n', 'ki18n5', 'kiconthemes', 'kiconthemes5', 'kidentitymanagement', 'kidletime', 'kig', 'kigo', 'killbots', 'kimageannotator', 'kimagemapeditor', 'kimap', 'kinfocenter', 'kinit', 'kio', 'kio-admin', 'kio-extras', 'kio-fuse', 'kio-gdrive', 'kio-zeroconf', 'kio5', 'kirigami', 'kirigami-addons', 'kirigami-gallery', 'kirigami2', 'kiriki', 'kitemmodels', 'kitemviews', 'kitemviews5', 'kiten', 'kitinerary', 'kjobwidgets', 'kjobwidgets5', 'kjournald', 'kjumpingcube', 'kldap', 'kleopatra', 'klettres', 'klickety', 'klines', 'kmag', 'kmahjongg', 'kmail', 'kmail-account-wizard', 'kmailtransport', 'kmbox', 'kmenuedit', 'kmime', 'kmines', 'kmix', 'kmod', 'kmousetool', 'kmouth', 'kmplot', 'knavalbattle', 'knetwalk', 'knewstuff', 'knewstuff5', 'knights', 'knotifications', 'knotifications5', 'knotifyconfig', 'koko', 'kolf', 'kollision', 'kolourpaint', 'kompare', 'kongress', 'konqueror', 'konquest', 'konsole', 'kontact', 'kontactinterface', 'kontrast', 'konversation', 'kopeninghours', 'korganizer', 'kosmindoormap', 'kpackage', 'kpackage5', 'kparts', 'kparts5', 'kpat', 'kpeople', 'kpimtextedit', 'kpipewire', 'kpkpass', 'kplotting', 'kplotting5', 'kpmcore', 'kpty', 'kpty5', 'kpublictransport', 'kqtquickcharts', 'kquickcharts', 'kquickimageeditor', 'krb5', 'krdc', 'krdp', 'krecorder', 'kreversi', 'krfb', 'kruler', 'krunner', 'ksanecore', 'kscreen', 'kscreenlocker', 'kservice', 'kservice5', 'kshisen', 'ksirk', 'ksmtp', 'ksnakeduel', 'kspaceduel', 'ksquares', 'ksshaskpass', 'kstatusnotifieritem', 'ksudoku', 'ksvg', 'ksystemlog', 'ksystemstats', 'kteatime', 'ktextaddons', 'ktexteditor', 'ktexteditor5', 'ktexttemplate', 'ktextwidgets', 'ktextwidgets5', 'ktimer', 'ktnef', 'ktorrent', 'ktouch', 'ktrip', 'ktuberling', 'kturtle', 'kubrick', 'kunifiedpush', 'kunitconversion', 'kunitconversion5', 'kuserfeedback', 'kwallet', 'kwallet-pam', 'kwallet5', 'kwalletmanager', 'kwave', 'kwayland', 'kweather', 'kweathercore', 'kwidgetsaddons', 'kwidgetsaddons5', 'kwin', 'kwindowsystem', 'kwindowsystem5', 'kwordquiz', 'kwrited', 'kxmlgui', 'kxmlgui5', 'lame', 'lapack', 'layer-shell-qt', 'lcms2', 'ldb', 'leancrypto', 'leptonica', 'less', 'libabw', 'libaccounts-glib', 'libaccounts-qt', 'libadwaita', 'libaec', 'libaio', 'libakonadi', 'libao', 'libarchive', 'libass', 'libass.so', 'libassuan', 'libasyncns', 'libatasmart', 'libatomic_ops', 'libavc1394', 'libavcodec.so', 'libavif', 'libavtp', 'libb2', 'libblockdev', 'libblockdev-crypto', 'libblockdev-fs', 'libblockdev-loop', 'libblockdev-mdraid', 'libblockdev-nvme', 'libblockdev-part', 'libblockdev-swap', 'libbluray', 'libbluray.so', 'libbpf', 'libbs2b', 'libbsd', 'libburn', 'libbytesize', 'libcaca', 'libcanberra', 'libcanberra-pulse', 'libcap', 'libcap-ng', 'libcbor', 'libcdio', 'libcdio-paranoia', 'libcdr', 'libcloudproviders', 'libcmis', 'libcolord', 'libcolord', 'libcrypt.so', 'libcue', 'libcups', 'libdaemon', 'libdatrie', 'libdav1d.so', 'libdbus-1.so', 'libdbusmenu-qt5', 'libdc1394', 'libdca', 'libde265', 'libdecor', 'libdeflate', 'libdisplay-info', 'libdmapsharing', 'libdmtx', 'libdovi', 'libdrm', 'libdv', 'libdvbpsi', 'libdvdnav', 'libdvdread', 'libe-book', 'libebml.so', 'libebur128', 'libedataserverui4', 'libedit', 'libegl', 'libei', 'libelf', 'libepoxy', 'libepubgen', 'libetonyek', 'libevdev', 'libevent', 'libexif', 'libexttextcat', 'libfabric', 'libfakekey', 'libfdk-aac', 'libffi', 'libfontenc', 'libfreeaptx', 'libfreehand', 'libftdi', 'libgcrypt', 'libgdata', 'libgdm', 'libgee', 'libgexiv2', 'libgirepository', 'libgirepository', 'libgl', 'libglvnd', 'libgme', 'libgoa', 'libgoa', 'libgpg-error', 'libgphoto2', 'libgravatar', 'libgsf', 'libgtop', 'libgudev', 'libgusb', 'libgweather-4', 'libgxps', 'libhandy', 'libheif', 'libibus', 'libical', 'libice', 'libidn', 'libidn2', 'libiec61883', 'libieee1284', 'libimagequant', 'libimobiledevice', 'libimobiledevice-glue', 'libinih', 'libinput', 'libinstpatch', 'libiptcdata', 'libisl.so', 'libixion', 'libjcat', 'libjpeg-turbo', 'libjson-glib-1.0.so', 'libjxl', 'libkcddb', 'libkcompactdisc', 'libkdcraw', 'libkdegames', 'libkdepim', 'libkeduvocdocument', 'libkexiv2', 'libkgapi', 'libkleo', 'libkmahjongg', 'libkolabxml', 'libkomparediff2', 'libksane', 'libksba', 'libkscreen', 'libksieve', 'libksysguard', 'libktorrent', 'liblangtag', 'liblc3', 'libldac', 'libldap', 'liblouis', 'liblqr', 'liblrdf', 'liblsmash.so', 'libltc', 'libltdl', 'libmad', 'libmalcontent', 'libmanette', 'libmatroska', 'libmaxminddb', 'libmbim', 'libmd', 'libmediaart', 'libmfx', 'libmicrodns', 'libmm-glib', 'libmm-glib', 'libmng', 'libmnl', 'libmodplug', 'libmpc', 'libmpcdec', 'libmpeg2', 'libmpfr.so', 'libmspub', 'libmsym', 'libmtp', 'libmusicbrainz5', 'libmwaw', 'libmysofa', 'libnautilus-extension.so', 'libndp', 'libnetfilter_conntrack', 'libnewt', 'libnfnetlink', 'libnfs', 'libnftnl', 'libnghttp2', 'libnghttp3', 'libnice', 'libnl', 'libnm', 'libnma-common', 'libnma-gtk4', 'libnotify', 'libnsl', 'libnumbertext', 'libnvme', 'liboauth', 'libodfgen', 'libogg', 'libolm', 'libopenmpt', 'liborcus', 'libosinfo', 'libp11-kit', 'libp11-kit', 'libpagemaker', 'libpam-google-authenticator', 'libpaper', 'libpcap', 'libpciaccess', 'libpeas', 'libpgm', 'libphonenumber', 'libpipeline', 'libpipewire', 'libpipewire', 'libplacebo', 'libplasma', 'libplist', 'libpng', 'libpolkit-gobject-1.so', 'libportal', 'libportal-gtk3', 'libportal-gtk4', 'libproxy', 'libpsl', 'libpulse', 'libpwquality', 'libqaccessibilityclient-qt6', 'libqalculate', 'libqmi', 'libqrtr-glib', 'libquotient', 'libqxp', 'libraqm', 'librav1e.so', 'libraw', 'libraw1394', 'libreoffice', 'librest', 'librevenge', 'librsvg', 'librsvg-2.so', 'libsamplerate', 'libsasl', 'libseccomp', 'libsecret', 'libshout', 'libshumate', 'libsigc++-3.0', 'libsixel', 'libsm', 'libsndfile', 'libsodium', 'libsoup', 'libsoup3', 'libsoxr', 'libspectre', 'libspeechd', 'libspelling', 'libsrtp', 'libssh', 'libssh2', 'libstaroffice', 'libstemmer', 'libsynctex', 'libsysprof-capture', 'libsystemd.so', 'libtar', 'libtasn1', 'libteam', 'libtevent.so', 'libthai', 'libtheora', 'libtiff', 'libtirpc', 'libtommath', 'libtool', 'libunibreak', 'libunistring', 'libunwind', 'libupnp', 'liburing', 'libusb', 'libusb-1.0.so', 'libusbmuxd', 'libutempter', 'libva', 'libva.so', 'libvdpau', 'libverto-module-base', 'libvidstab.so', 'libvisio', 'libvlc', 'libvncserver', 'libvorbis', 'libvpx', 'libvpx.so', 'libwacom', 'libwbclient', 'libwebkitgtk-6.0.so', 'libwebp', 'libwireplumber', 'libwnck3', 'libwpd', 'libwps', 'libx11', 'libx264.so', 'libx265.so', 'libxau', 'libxaw', 'libxcb', 'libxcomposite', 'libxcrypt', 'libxcursor', 'libxcvt', 'libxdamage', 'libxdmcp', 'libxext', 'libxfixes', 'libxfont2', 'libxft', 'libxi', 'libxi', 'libxinerama', 'libxkbcommon', 'libxkbcommon-x11', 'libxkbfile', 'libxml2', 'libxmlb', 'libxmu', 'libxpm', 'libxpresent', 'libxrandr', 'libxrender', 'libxres', 'libxshmfence', 'libxslt', 'libxss', 'libxt', 'libxtables.so', 'libxtst', 'libxv', 'libxvidcore.so', 'libxxf86vm', 'libxxhash.so', 'libyaml', 'libyuv', 'libzimg.so', 'libzip', 'libzmf', 'licenses', 'lilv', 'linux', 'linux-api-headers', 'linux-firmware', 'linux-firmware-whence', 'linux-hardened', 'linux-hardened-headers', 'linux-headers', 'linux-lts', 'linux-lts-headers', 'llvm', 'llvm-libs', 'lm_sensors', 'lmdb', 'localsearch', 'lokalize', 'loupe', 'lpsolve', 'lskat', 'lua', 'luajit', 'lv2', 'lvm2', 'lz4', 'lzo', 'm4', 'maeparser', 'mailcommon', 'mailimporter', 'make', 'malcontent', 'man', 'marble', 'marble-common', 'mariadb', 'mariadb-clients', 'mariadb-libs', 'markdownpart', 'massif-visualizer', 'mbox-importer', 'md4c', 'mdadm', 'media-player-info', 'merkuro', 'mesa', 'mesa-utils', 'messagelib', 'milou', 'mime-types', 'mimetreeparser', 'minizip', 'minuet', 'mjpegtools', 'mkinitcpio-busybox', 'mlt', 'mobile-broadband-provider-info', 'mod_dnssd', 'modemmanager', 'modemmanager-qt', 'mokutil', 'molequeue', 'mpdecimal', 'mpfr', 'mpg123', 'mpv', 'mpvqt', 'msgraph', 'mtdev', 'mujs', 'mutter', 'nano', 'nautilus', 'ncurses', 'neochat', 'neon', 'neon', 'net-snmp', 'netpbm', 'nettle', 'networkmanager', 'networkmanager-openvpn', 'networkmanager-qt', 'noto-fonts', 'npth', 'nspr', 'nss', 'ntfs-3g', 'numactl', 'ocean-sound-theme', 'ocl-icd', 'okular', 'onetbb', 'onevpl', 'openal', 'openbabel', 'opencl-icd-loader', 'opencore-amr', 'opencv', 'openexr', 'openh264', 'openjpeg2', 'openmpi', 'openpmix', 'openssh', 'openssl', 'openucx', 'openvpn', 'openxr', 'opus', 'orc', 'orca', 'org.freedesktop.secrets', 'osinfo-db', 'ostree', 'oxygen', 'oxygen-sounds', 'p11-kit', 'pacman', 'pacman-mirrorlist', 'pahole', 'palapeli', 'pam', 'pambase', 'pango', 'pangomm-2.48', 'parley', 'parted', 'partitionmanager', 'passim', 'patch', 'pciutils', 'pcre', 'pcre2', 'pcsclite', 'perl', 'perl-error', 'perl-mailtools', 'perl-timedate', 'phonon-qt6', 'phonon-qt6-backend', 'picmi', 'pim-data-exporter', 'pim-sieve-editor', 'pimcommon', 'pinentry', 'pipewire', 'pipewire', 'pipewire-audio', 'pipewire-pulse', 'pipewire-session-manager', 'pixman', 'pkcs11-helper', 'pkgconf', 'plasma', 'plasma-activities', 'plasma-activities-stats', 'plasma-browser-integration', 'plasma-desktop', 'plasma-disks', 'plasma-firewall', 'plasma-integration', 'plasma-nm', 'plasma-pa', 'plasma-sdk', 'plasma-systemmonitor', 'plasma-thunderbolt', 'plasma-vault', 'plasma-welcome', 'plasma-workspace', 'plasma-workspace-wallpapers', 'plasma5support', 'plasmatube', 'plymouth', 'plymouth-kcm', 'polkit', 'polkit-kde-agent', 'polkit-qt5', 'polkit-qt6', 'poppler', 'poppler', 'poppler-data', 'poppler-glib', 'poppler-qt6', 'popt', 'portaudio', 'postgresql-libs', 'powerdevil', 'poxml', 'ppp', 'print-manager', 'prison', 'procps-ng', 'protobuf', 'protobuf-c', 'prrte', 'psmisc', 'pugixml', 'pulse-native-provider', 'pulseaudio-qt', 'purpose', 'purpose5', 'python', 'python-argcomplete', 'python-attrs', 'python-autocommand', 'python-automat', 'python-cairo', 'python-certifi', 'python-cffi', 'python-charset-normalizer', 'python-click', 'python-constantly', 'python-cryptography', 'python-darkdetect', 'python-dbus', 'python-defusedxml', 'python-dlib', 'python-dotenv', 'python-filelock', 'python-gobject', 'python-greenlet', 'python-hyperlink', 'python-idna', 'python-incremental', 'python-jaraco.collections', 'python-jaraco.context', 'python-jaraco.functools', 'python-jaraco.text', 'python-legacy-cgi', 'python-more-itertools', 'python-numpy', 'python-opencv', 'python-packaging', 'python-pefile', 'python-pexpect', 'python-pillow', 'python-pip', 'python-platformdirs', 'python-psutil', 'python-psycopg2', 'python-ptyprocess', 'python-pycparser', 'python-pygdbmi', 'python-pyxdg', 'python-qrcode', 'python-qtpy', 'python-requests', 'python-sentry_sdk', 'python-setproctitle', 'python-setuptools', 'python-sqlalchemy', 'python-twisted', 'python-typing_extensions', 'python-urllib3', 'python-wheel', 'python-ytmusicapi', 'python-zope-interface', 'qca-qt5', 'qca-qt6', 'qcoro', 'qgpgme-qt6', 'qhull', 'qqc2-breeze-style', 'qqc2-desktop-style', 'qrencode', 'qt5-base', 'qt5-declarative', 'qt5-graphicaleffects', 'qt5-multimedia', 'qt5-quickcontrols', 'qt5-quickcontrols2', 'qt5-script', 'qt5-speech', 'qt5-svg', 'qt5-translations', 'qt5-wayland', 'qt5-x11extras', 'qt5-xmlpatterns', 'qt6-5compat', 'qt6-base', 'qt6-charts', 'qt6-connectivity', 'qt6-declarative', 'qt6-httpserver', 'qt6-imageformats', 'qt6-location', 'qt6-multimedia', 'qt6-multimedia-backend', 'qt6-multimedia-gstreamer', 'qt6-networkauth', 'qt6-positioning', 'qt6-python-bindings', 'qt6-quick3d', 'qt6-quicktimeline', 'qt6-scxml', 'qt6-sensors', 'qt6-shadertools', 'qt6-speech', 'qt6-svg', 'qt6-tools', 'qt6-translations', 'qt6-virtualkeyboard', 'qt6-wayland', 'qt6-webchannel', 'qt6-webengine', 'qt6-websockets', 'qt6-webview', 'qtkeychain-qt6', 'raptor', 'rasqal', 'rav1e', 're2', 'readline', 'recastnavigation', 'redland', 'ripgrep', 'ripgrep-all', 'rocs', 'rtkit', 'rtmpdump', 'rubberband', 'run-parts', 'rygel', 'samba', 'sane', 'sbc', 'sbctl', 'sbsigntools', 'sddm', 'sddm-kcm', 'sdl2', 'sdl2_ttf', 'sdl3', 'sed', 'serd', 'sh', 'shaderc', 'shadow', 'shared-mime-info', 'shiboken6', 'shim-signed', 'signon-kwallet-extension', 'signon-plugin-oauth2', 'signon-ui', 'signond', 'simple-scan', 'skanlite', 'skanpage', 'skladnik', 'slang', 'smartmontools', 'smbclient', 'smbclient', 'smbclient', 'snappy', 'snapshot', 'socat', 'solid', 'solid5', 'sonnet', 'sonnet5', 'sord', 'sound-theme-freedesktop', 'soundtouch', 'source-highlight', 'spandsp', 'spectacle', 'speech-dispatcher', 'speex', 'speexdsp', 'spglib', 'spirv-tools', 'sqlite', 'sratom', 'srt', 'startup-notification', 'step', 'sudo', 'sushi', 'svgpart', 'svt-av1', 'svt-hevc', 'sweeper', 'syndication', 'syndication5', 'syntax-highlighting', 'syntax-highlighting5', 'systemd', 'systemd', 'systemd-libs', 'systemd-libs', 'systemd-sysvcompat', 'systemd-ukify', 'systemsettings', 'taglib', 'talloc', 'tar', 'tbb', 'tcl', 'tdb', 'tecla', 'telly-skout', 'tessdata', 'tesseract', 'tesseract-data-osd', 'texinfo', 'thin-provisioning-tools', 'threadweaver', 'tinysparql', 'tk', 'tokodon', 'totem', 'totem-pl-parser', 'totem-plparser', 'tpm2-tss', 'tslib', 'ttf-font', 'ttf-hack', 'ttf-liberation', 'twolame', 'tzdata', 'uchardet', 'udisks2', 'ufw', 'umbrello', 'unzip', 'upower', 'usbmuxd', 'util-linux', 'util-linux-libs', 'util-linux-libs', 'v4l-utils', 'vapoursynth', 'verdict', 'vid.stab', 'vim', 'vim-runtime', 'vlc', 'vmaf', 'volume_key', 'vte-common', 'vte4', 'vtk', 'vulkan-icd-loader', 'vulkan-tools', 'wacomtablet', 'wavpack', 'wayland', 'wayland-utils', 'webkit2gtk-4.1', 'webkitgtk-6.0', 'webrtc-audio-processing-1', 'which', 'wildmidi', 'wireplumber', 'woff2', 'wpa_supplicant', 'wsdd', 'x264', 'x265', 'xapian-core', 'xcb-proto', 'xcb-util', 'xcb-util-cursor', 'xcb-util-image', 'xcb-util-keysyms', 'xcb-util-renderutil', 'xcb-util-wm', 'xdg-dbus-proxy', 'xdg-desktop-portal', 'xdg-desktop-portal-gnome', 'xdg-desktop-portal-gtk', 'xdg-desktop-portal-kde', 'xdg-user-dirs', 'xdg-user-dirs-gtk', 'xdg-utils', 'xerces-c', 'xf86-input-libinput', 'xf86-input-wacom', 'xf86-video-vesa', 'xkeyboard-config', 'xmlsec', 'xorg', 'xorg-bdftopcf', 'xorg-docs', 'xorg-font-util', 'xorg-fonts-100dpi', 'xorg-fonts-75dpi', 'xorg-fonts-alias-100dpi', 'xorg-fonts-alias-75dpi', 'xorg-fonts-encodings', 'xorg-iceauth', 'xorg-mkfontscale', 'xorg-server', 'xorg-server-common', 'xorg-server-devel', 'xorg-server-xephyr', 'xorg-server-xnest', 'xorg-server-xvfb', 'xorg-sessreg', 'xorg-setxkbmap', 'xorg-smproxy', 'xorg-util-macros', 'xorg-x11perf', 'xorg-xauth', 'xorg-xbacklight', 'xorg-xcmsdb', 'xorg-xcursorgen', 'xorg-xdpyinfo', 'xorg-xdriinfo', 'xorg-xev', 'xorg-xgamma', 'xorg-xhost', 'xorg-xinput', 'xorg-xkbcomp', 'xorg-xkbevd', 'xorg-xkbutils', 'xorg-xkill', 'xorg-xlsatoms', 'xorg-xlsclients', 'xorg-xmessage', 'xorg-xmodmap', 'xorg-xpr', 'xorg-xprop', 'xorg-xrandr', 'xorg-xrdb', 'xorg-xrefresh', 'xorg-xset', 'xorg-xsetroot', 'xorg-xvinfo', 'xorg-xwayland', 'xorg-xwd', 'xorg-xwininfo', 'xorg-xwud', 'xorgproto', 'xsettingsd', 'xvidcore', 'xxhash', 'xz', 'yakuake', 'yelp', 'yelp-xsl', 'yt-dlp', 'zanshin', 'zbar', 'zeromq', 'zix', 'zlib', 'zstd', 'zvbi', 'zxing-cpp']

# --- Global Language Object ---
lang: Locale = Locale("en") # Default, will be updated

# --- Argument Parsing ---
def setup_arg_parser():
    parser = ArgumentParser(prog="Secux Linux Builder", description=f"{lang.build} ISO {lang.workdir} Secux Linux // Программа для сборки ISO образа дистрибутива Secux Linux")
    parser.add_argument('-r', '--russian', help="использовать русский язык в GUI", action=BooleanOptionalAction)
    parser.add_argument('-c', '--cli', help="disable GUI | отключить графический режим", action=BooleanOptionalAction, default=False)
    parser.add_argument('-n', '--online', help="create online build // создать онлайн сборку", action=BooleanOptionalAction)
    parser.add_argument('-f', '--offline', help="create offline build // создать офлайн сборку", action=BooleanOptionalAction)
    parser.add_argument('-b', '--bin', help="work directory for building // рабочая папка для сборки", default=os.path.join(WORKDIR, "bin"))
    parser.add_argument('-o', '--output', help="directory for ISO images // папка для ISO образов", default=os.path.join(WORKDIR, "builds"))
    parser.add_argument('-u', '--update-offline-software', help="update offline software // обновить офлайн ПО", action="store_true", default=False)
    parser.add_argument('-i', '--update-offline-repo', help="update offline repositories // обновить офлайн репозиторий", action="store_true", default=False)
    parser.add_argument('-s', '--scaling', help="GUI scaling (in percents, example: -s 100) // масштабирование графического интерфейса (в процентах, например: -s 100)", default="100")
    parser.add_argument('-d', '--dark-theme', help="use dark theme // использовать темную тему", action='store_true', default=False)
    parser.add_argument('--version', help="show version and exit // показать версию и выйти", action="store_true", default=False)
    parser.add_argument('--install-all-dependencies', help="install all dependencies and exit // установить все зависимости и выйти", action='store_true', default=False)
    return parser.parse_args()


def check_critical_dependencies():
    """Checks for non-Python dependencies essential for basic operation."""
    if not os.path.isfile("/usr/bin/pacman"):
        print(f"[ERROR] {lang.arch_based}")
        sys.exit(1)
    if os.geteuid() != 0:
        print(f"[ERROR] {lang.root}!")
        sys.exit(1)
    # Add other critical checks if needed (e.g., git?)

def install_dependencies():
    """Installs required packages using pacman and pip."""
    needed_pacman = ['archiso', 'python-pip', 'python-pillow', 'git', 'bash', 'rsync', 'python-requests', 'python-packaging', 'python-darkdetect', 'tk']
    needed_pip = ['customtkinter']
    try:
        # Use check=True to raise an error if pacman fails
        subprocess.run(["/usr/bin/pacman", '-Syu', '--needed', '--noconfirm'] + needed_pacman, check=True)
        # Use check=True for pip as well
        subprocess.run(['/usr/bin/pip', 'install'] + needed_pip + ['--break-system-packages'], check=True)
        print(f"[INFO] {lang.deps_success}.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {lang.deps_err}: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"[ERROR] {lang.deps_fnfe} {e}")
        sys.exit(1)

# --- GUI Notification Class ---
# Needs customtkinter, so import it here
try:
    from customtkinter import *
    from PIL import Image
    gui_available = True
except ImportError:
    gui_available = False

class Notification(CTkToplevel if gui_available else object):
    def __init__(self, message: str, title: str = lang.notification, icon: str = "warning.png", message_bold: bool = False, exit_btn_msg: str = lang.exit, app_instance=None):
        # If GUI is not available or running in CLI mode, just print
        if not gui_available or (app_instance and app_instance.is_cli):
             prefix = f"[{title.upper()}]" if title else "[NOTIFICATION]"
             print(f"{prefix} {message}", file=sys.stderr if "error" in title.lower() else sys.stdout)
             return

        # Proceed with GUI notification
        try:
            super().__init__()
            self.app = app_instance # Store reference if needed
            self.lang = self.app.lang if self.app else lang # Use app's lang if available

            self.title(title if title else self.lang.info) # Use translated title
            icon_path = Path(WORKDIR) / "images" / icon
            if icon_path.is_file():
                img = Image.open(icon_path)
                image = CTkImage(light_image=img, dark_image=img, size=(60, 60)) # Smaller icon
                image_label = CTkLabel(self, text="", image=image)
                image_label.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
                label_col = 1
            else:
                print(f"[WARNING] {self.lang.icon_not_found} {icon_path}")
                label_col = 0 # Span label if no icon

            label = CTkLabel(self, text=message, wraplength=350) # Wrap long messages
            if message_bold:
                label.configure(font=(None, 13, "bold")) # Adjusted font size
            label.grid(row=0, column=label_col, padx=15, pady=10, sticky="nsew")

            exit_button = CTkButton(self, text=exit_btn_msg if exit_btn_msg else "OK", command=self.destroy)
            exit_button.grid(row=1, column=0, columnspan=label_col + 1, padx=15, pady=(5, 10), sticky="nsew")

            self.bind("<Return>", lambda event: self.destroy())
            self.grab_set() # Make modal
            self.lift()
            self.attributes("-topmost", True) # Try to bring to front
            self.update_idletasks() # Ensure size is calculated
            # Center window (optional)
            # x = self.master.winfo_rootx() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
            # y = self.master.winfo_rooty() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
            # self.geometry(f"+{x}+{y}")

        except Exception as e:
            print(f"[ERROR] {self.lang.notify_gui_fail}: {e}", file=sys.stderr)
            print(f"[NOTIFICATION] [{title.upper()}] {message}", file=sys.stderr)


# --- Main Application Class ---
class App(CTk if gui_available else object):
    def __init__(self, args, lang_obj: Locale):
        self.args = args
        self.lang = lang_obj
        self.is_cli = args.cli or not gui_available
        self.build_failed_flag = False # Flag to stop processing on error
        self.worker_thread = None
        self.task_queue = None
        self.gui_console = None # Textbox widget for GUI console
        self._current_task_result = None
        self._current_task_exception = None
        self._stop_worker = threading.Event() # To signal worker thread termination

        self.repos = {
            "secux-installer": "https://github.com/kolbanidze/secux-installer.git",
            "secux-apps": "https://github.com/kolbanidze/secux-apps.git",
            "KIRTapp": "https://github.com/kirt-king/test_app.git"
            }

        # --- Path Setup ---
        self.bin_dir = self._setup_dir(args.bin, "bin", self.lang.workdir)
        self.output_dir = self._setup_dir(args.output, "builds", self.lang.isoimagesfolder)


        if self.is_cli:
            print(f"[INFO] {self.lang.cli_on}")
            # CLI mode: Execute directly
            self._run_cli()
        else:
            # GUI mode: Setup UI
            if not gui_available:
                 # Should not happen if checks pass, but safeguard
                 print(f"[ERROR] {lang.gui_error}")
                 sys.exit(1)

            self._setup_gui()

    def _setup_dir(self, path_arg, default_subdir, description):
        """Validates and creates directory, returns absolute path."""
        path = os.path.realpath(path_arg)
        if not os.path.isdir(path):
            self.log(f"[INFO] {description} {self.lang.dir_not_found_at} '{path}'. {self.lang.attempting_to_create}.")
            try:
                os.makedirs(path, exist_ok=True)
                self.log(f"[INFO] {self.lang.created_dir}: {path}")
            except OSError as e:
                self.log(f"[ERROR] {self.lang.failed_to_create_dir} {path}: {e}", level="error")
                # Fallback to default relative path if creation fails
                fallback_path = os.path.join(WORKDIR, default_subdir)
                self.log(f"[WARNING] {self.lang.dir_fallback}: {fallback_path}")
                try:
                    os.makedirs(fallback_path, exist_ok=True)
                    return fallback_path
                except OSError as e_fb:
                     self.log(f"[ERROR] {self.lang.failed_to_create_dir} {fallback_path}: {e_fb}", level="error")
                     self.report_error(f"{self.lang.failed_to_create_dir} {fallback_path}. {self.lang.check_console_log}", exit_on_error=True)
                     return "" # Should exit before returning
        return path


    def log(self, message: str, level="info"):
        """Logs message to console (and GUI console if available)."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        # Always print to standard console
        print(log_entry, end='', file=sys.stderr if level == "error" else sys.stdout)

        # Update GUI console safely if it exists
        if not self.is_cli and hasattr(self, 'gui_console') and self.gui_console:
             self.after(0, self._update_gui_console, log_entry)

    def _update_gui_console(self, text: str):
        """Safely updates the GUI console Textbox from the main thread."""
        if self.gui_console and self.gui_console.winfo_exists():
            try:
                self.gui_console.configure(state="normal")
                self.gui_console.insert("end", text)
                self.gui_console.see("end")
                self.gui_console.configure(state="disabled")
            except Exception as e:
                # Fallback if GUI update fails
                print(f"ERROR (update_gui_console): {e}\n{text}", file=sys.stderr)

    def report_error(self, message: str, exit_on_error: bool = False, show_notification: bool = True):
        """Logs error and optionally shows GUI notification and exits."""
        self.log(f"[ERROR] {message}", level="error")
        self.build_failed_flag = True # Mark build as failed

        if show_notification and not self.is_cli:
             Notification(message, title=self.lang.error, icon="warning.png", app_instance=self, exit_btn_msg="OK")

        if exit_on_error:
            self.log(f"[INFO] {self.lang.build_interrupted}", level="error")
            self._cleanup_resources() # Attempt cleanup before exit
            sys.exit(1)

    def _cleanup_resources(self):
        """Cleans up resources like the worker thread."""
        if self.worker_thread and self.worker_thread.is_alive():
            self.log(f"[INFO] {self.lang.stopping_worker_thread}...")
            self._stop_worker.set() # Signal thread to stop
            self.task_queue.put(None) # Send sentinel value

    def _run_cli(self):
        """Executes the build process in CLI mode."""
        self.log(f"[INFO] Secux Linux Builder v{VERSION} (CLI)")

        if not self._pre_build_checks():
            self.report_error(self.lang.check_console_log, exit_on_error=True)
            return # Exit happens in report_error

        self.build_failed_flag = False # Reset flag before starting

        # Execute build steps sequentially
        success = self._perform_build_steps(
            update_apps=self.args.update_offline_software,
            update_repo=self.args.update_offline_repo,
            online_build=self.args.online,
            offline_build=self.args.offline
        )

        if success and not self.build_failed_flag:
            self.log(f"[INFO] {self.lang.build_complete_success}")
        else:
            self.log(f"[ERROR] {self.lang.build_interrupted} {self.lang.check_console_log}", level="error")
            sys.exit(1)

    def _setup_gui(self):
        """Sets up the CustomTkinter GUI."""
        # from customtkinter import set_widget_scaling, set_window_scaling, set_appearance_mode
        # from customtkinter import CTkLabel, CTkButton, CTkCheckBox, CTkOptionMenu, CTkTextbox
        from tkinter import filedialog # Keep standard filedialog

        # Apply scaling
        try:
            scaling_val = int(self.args.scaling)
            if not 80 <= scaling_val <= 500: # Basic range check
                raise ValueError(self.lang.scale_error)
            scaling_float = round(scaling_val / 100, 2)
            set_widget_scaling(scaling_float)
            set_window_scaling(scaling_float)
        except ValueError:
            self.log(f"[WARNING] {self.lang.scaling_error}", level="error")
            scaling_val = 100
            scaling_float = 1.0
            set_widget_scaling(scaling_float)
            set_window_scaling(scaling_float)

        if self.args.dark_theme:
            set_appearance_mode("dark")

        # Initialize CTk window
        super().__init__()
        self.title("Secux Linux Builder")

        # --- Widgets ---
        row = 0
        label = CTkLabel(self, text="Secux Linux Builder", font=(None, 16, 'bold'))
        label.grid(row=row, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="nsew")
        row += 1

        self.work_dir_label = CTkLabel(self, text=f"{self.lang.workdir}: {self.bin_dir}")
        self.work_dir_label.grid(row=row, column=0, padx=15, pady=5, sticky="w")
        self.work_dir_btn = CTkButton(self, text=self.lang.changedir, command=self._gui_select_bin_dir)
        self.work_dir_btn.grid(row=row, column=1, padx=15, pady=5, sticky="ew")
        row += 1

        self.output_dir_label = CTkLabel(self, text=f"{self.lang.isoimagesfolder}: {self.output_dir}")
        self.output_dir_label.grid(row=row, column=0, padx=15, pady=5, sticky="w")
        self.output_dir_btn = CTkButton(self, text=self.lang.changedir, command=self._gui_select_output_dir)
        self.output_dir_btn.grid(row=row, column=1, padx=15, pady=5, sticky="ew")
        row += 1

        self.online_checkbox = CTkCheckBox(self, text=self.lang.online_build)
        if self.args.online: self.online_checkbox.select()
        self.online_checkbox.grid(row=row, column=0, padx=15, pady=5, sticky="w")
        self.online_label = CTkLabel(self, text=self.lang.online_label, wraplength=250, justify="left")
        self.online_label.grid(row=row, column=1, padx=15, pady=5, sticky="w")
        row += 1

        self.offline_checkbox = CTkCheckBox(self, text=self.lang.offline_build)
        if self.args.offline: self.offline_checkbox.select()
        self.offline_checkbox.grid(row=row, column=0, padx=15, pady=5, sticky="w")
        self.offline_label = CTkLabel(self, text=self.lang.offline_label, wraplength=250, justify="left")
        self.offline_label.grid(row=row, column=1, padx=15, pady=5, sticky="w")
        row += 1

        self.update_offline_apps_checkbox = CTkCheckBox(self, text=self.lang.update_apps)
        if self.args.update_offline_software: self.update_offline_apps_checkbox.select()
        self.update_offline_apps_checkbox.grid(row=row, column=0, padx=15, pady=5, sticky="w")
        self.update_offline_apps_label = CTkLabel(self, text="Secux Installer, Secux Manager, KIRTapp", wraplength=250, justify="left")
        self.update_offline_apps_label.grid(row=row, column=1, padx=15, pady=5, sticky="w")
        row += 1

        self.update_offline_repo_checkbox = CTkCheckBox(self, text=self.lang.offline_repo)
        if self.args.update_offline_repo: self.update_offline_repo_checkbox.select()
        self.update_offline_repo_checkbox.grid(row=row, column=0, padx=15, pady=5, sticky="w")
        self.update_offline_repo_label = CTkLabel(self, text=self.lang.offline_os, wraplength=250, justify="left")
        self.update_offline_repo_label.grid(row=row, column=1, padx=15, pady=5, sticky="w")
        row += 1

        self.language_menu = CTkOptionMenu(self, values=["English", "Русский"], command=self._gui_language_handler)
        if self.lang.CURRENT_LANGUGAGE == "ru": self.language_menu.set("Русский")
        else: self.language_menu.set("English")
        self.language_menu.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        self.language_label = CTkLabel(self, text="Language // Язык")
        self.language_label.grid(row=row, column=1, padx=15, pady=5, sticky="w")
        row += 1

        self.scaling_menu = CTkOptionMenu(self, values=["80%", "100%", "125%", "150%", "200%"], command=self._gui_scaling_handler)
        self.scaling_menu.set(f"{scaling_val}%")
        self.scaling_menu.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        self.scaling_label = CTkLabel(self, text=self.lang.scaling)
        self.scaling_label.grid(row=row, column=1, padx=15, pady=5, sticky="w")
        row += 1

        self.build_button = CTkButton(self, text=self.lang.build, command=self._gui_start_build)
        self.build_button.grid(row=row, column=0, columnspan=2, padx=15, pady=(10, 10), sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_gui_close)

    def _on_gui_close(self):
        """Handler for GUI window closing."""
        self._cleanup_resources()
        self.destroy()

    def _gui_language_handler(self, choice: str):
        """Updates language and GUI text."""
        global lang # Update global lang object too, for consistency
        if choice == "Русский" and self.lang.CURRENT_LANGUGAGE != "ru":
            self.lang = Locale("ru")
            lang = self.lang
            self._gui_update_text()
        elif choice == "English" and self.lang.CURRENT_LANGUGAGE != "en":
            self.lang = Locale("en")
            lang = self.lang
            self._gui_update_text()

    def _gui_update_text(self):
        """Refreshes all translatable text widgets in the GUI."""
        self.work_dir_label.configure(text=f"{self.lang.workdir}: {self.bin_dir}")
        self.work_dir_btn.configure(text=self.lang.changedir)
        self.output_dir_label.configure(text=f"{self.lang.isoimagesfolder}: {self.output_dir}")
        self.output_dir_btn.configure(text=self.lang.changedir)
        self.online_checkbox.configure(text=self.lang.online_build)
        self.online_label.configure(text=self.lang.online_label)
        self.offline_checkbox.configure(text=self.lang.offline_build)
        self.offline_label.configure(text=self.lang.offline_label)
        self.update_offline_apps_checkbox.configure(text=self.lang.update_apps)
        self.update_offline_repo_checkbox.configure(text=self.lang.offline_repo)
        self.update_offline_repo_label.configure(text=self.lang.offline_os)
        self.scaling_label.configure(text=self.lang.scaling)
        self.build_button.configure(text=self.lang.build)

    def _gui_scaling_handler(self, new_scaling: str):
        """Applies new UI scaling."""
        # from customtkinter import set_widget_scaling, set_window_scaling
        try:
            scale_int = int(new_scaling.replace("%", ""))
            scale_float = round(scale_int / 100, 2)
            set_widget_scaling(scale_float)
            set_window_scaling(scale_float)
        except ValueError:
            self.log(f"[ERROR] {self.lang.scale_invalid}: {new_scaling}", level="error")

    def _gui_select_bin_dir(self):
        """Opens dialog to select binary/work directory."""
        from tkinter import filedialog
        dir_path = filedialog.askdirectory(mustexist=True, initialdir=self.bin_dir, title=self.lang.workdir)
        if dir_path:
            self.bin_dir = os.path.realpath(dir_path)
            self.work_dir_label.configure(text=f"{self.lang.workdir}: {self.bin_dir}")

    def _gui_select_output_dir(self):
        """Opens dialog to select output/ISO directory."""
        from tkinter import filedialog
        dir_path = filedialog.askdirectory(mustexist=True, initialdir=self.output_dir, title=self.lang.isoimagesfolder)
        if dir_path:
            self.output_dir = os.path.realpath(dir_path)
            self.output_dir_label.configure(text=f"{self.lang.isoimagesfolder}: {self.output_dir}")

    def _gui_start_build(self):
        """Starts the build process in GUI mode."""

        if not self._pre_build_checks():
             return

        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("700x500")

        try:
             calm_img_path = Path(WORKDIR) / "images" / "calm.png"
             if calm_img_path.is_file():
                calm_img = Image.open(calm_img_path)
                calm_emoji = CTkImage(light_image=calm_img, dark_image=calm_img, size=(80, 80))
                calm_emoji_label = CTkLabel(self, text="", image=calm_emoji)
                calm_emoji_label.pack(padx=10, pady=10)
        except Exception as e:
            self.log(f"[WARNING] {self.lang.couldnt_load_image} 'calm.png': {e}")

        label = CTkLabel(self, text=self.lang.building)
        # label.grid(row=0, column=0, padx=10, pady=10, sticky="s") # Below icon if exists
        label.pack(padx=10, pady=10)

        self.gui_console = CTkTextbox(self, wrap='word', state='disabled', font=("monospace", 11))
        # self.gui_console.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.gui_console.pack(padx=10, pady=10, fill='both', expand=True)

        # --- Start Worker Thread ---
        self.build_failed_flag = False # Reset flag
        self._stop_worker.clear()
        self.task_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

        # --- Queue Build Task ---
        # We execute the main build logic as a function in the worker thread
        build_args = {
            "update_apps": self.update_offline_apps_checkbox.get(),
            "update_repo": self.update_offline_repo_checkbox.get(),
            "online_build": self.online_checkbox.get(),
            "offline_build": self.offline_checkbox.get()
        }
        self.execute_function(self._perform_build_steps, kwargs=build_args)
        # The result (True/False) will be handled by the worker loop's completion logic

    # --- Core Build Logic (Common to CLI and GUI worker) ---

    def _pre_build_checks(self) -> bool:
        """Performs checks required before starting the build."""
        # if not (self.args.online or self.args.offline or self.args.update_offline_software or self.args.update_offline_repo):
        #      msg = "No build type selected (use -n or -f) and no update tasks requested (use -u or -i)."
        #      if self.is_cli:
        #          print(f"[ERROR] {msg}")
        #      else:
        #          Notification(msg, title=self.lang.error, app_instance=self)
        #      return False

        if not Path(f"{WORKDIR}/releng").is_dir():
            self.report_error(self.lang.releng_error, show_notification=True)
            return False

        if not self._check_internet_connection():
            self.report_error(self.lang.internet_error, show_notification=True)

        if not self._check_dependencies():
            self.report_error(f"{self.lang.not_installed_deps} {self.lang.check_console_log}", show_notification=True)
            return False

        return True

    def _check_dependencies(self) -> bool:
        """Checks for required command-line tools."""
        # Check critical tools needed for the build process itself
        requirements = {
            "/usr/bin/mkarchiso": "archiso",
            "/usr/bin/git": "git",
            "/usr/bin/rsync": "rsync",
            "/usr/bin/pacman-key": "pacman",
            "/usr/bin/repo-add": "pacman",
            # Add others if strictly needed by the builder script itself
        }
        errors = False
        notification_pool = ""
        self.log(f"[INFO] {self.lang.checking_deps}...")
        for path, package in requirements.items():
            if not Path(path).is_file():
                text = f"{path} ({package}) {self.lang.not_installed_use} pacman -S {package}"
                self.log(f"[ERROR] {text}", level="error")
                notification_pool += f"- {package}\n"
                errors = True

        if errors:
            self.log(f"[ERROR] {self.lang.missing_deps} --install-all-dependencies", level="error")
            # Notification shown by caller (_pre_build_checks -> report_error)
            return False

        self.log(f"[INFO] {self.lang.deps_check_pass}.")
        return True

    def _check_internet_connection(self) -> bool:
        """Checks for a basic internet connection."""
        try:
            # Use requests if available (handles proxies better potentially)
            import requests
            response = requests.get("https://gstatic.com/generate_204", timeout=5)
            return response.status_code == 204
        except ImportError:
             # Fallback to subprocess ping if requests is not installed (should be though)
             try:
                 # Ping a reliable host, timeout after 2s, count 1 packet
                 process = subprocess.run(['/usr/bin/ping', '-c', '1', '-W', '2', '8.8.8.8'],
                                          stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL,
                                          check=False) # Don't throw error on failure
                 return process.returncode == 0
             except FileNotFoundError:
                 self.log(f"[WARNING] {self.lang.ping_fail}.", level="warning")
                 return False # Assume no connection if ping fails
             except Exception as e:
                 self.log(f"[WARNING] {self.lang.internet_check_error}: {e}", level="warning")
                 return False
        except requests.exceptions.RequestException as e:
            self.log(f"[INFO] {self.lang.internet_check_error}: {e}", level="info") 
            return False
    def _check_kolbanidze_key(self) -> bool:
        """Checks if the Kolbanidze PGP key is trusted. Uses direct worker call."""
        key_id = "CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE"
        command = ['/usr/bin/pacman-key', '--list-keys', key_id]
        try:
            # Directly use the worker execution method
            result = self._run_command_in_worker(command, None, suppress_output=True)
            return result == 0
        except Exception as e:
            self.log(f"[ERROR] {self.lang.pacman_check_error} {key_id}: {e}", level="error")
            # Ensure build fails if key check has an exception
            self.build_failed_flag = True
            return False

    def _add_kolbanidze_key(self) -> bool:
        """Attempts to add the Kolbanidze key. Uses direct worker call."""
        self.log(f"[INFO] {self.lang.kolbanidze_key_missing}")
        keyring_path = Path(WORKDIR) / "releng/airootfs/usr/share/pacman/keyrings"
        kolbanidze_gpg = keyring_path / "kolbanidze-keyring.gpg" # Example filename

        # Check path directly (worker context)
        if not kolbanidze_gpg.exists():
             self.report_error(f"{self.lang.keyring_error}: {kolbanidze_gpg}", show_notification=False)
             return False # report_error sets build_failed_flag

        command = ["/usr/bin/pacman-key", '--populate', '--keyring', 'kolbanidze', str(kolbanidze_gpg)]
        # Directly use the worker execution method
        result_pop = self._run_command_in_worker(command, None, suppress_output=False)
        if result_pop != 0:
            self.report_error(f"{self.lang.kolbanidze_key_add_fail} ({result_pop}).", show_notification=False)
            return False # report_error sets build_failed_flag

        self.log(f"[INFO] {self.lang.kolbanidze_key_ok}")
        return True

    def _perform_build_steps(self, update_apps: bool, update_repo: bool, online_build: bool, offline_build: bool) -> bool:
        """Orchestrates the actual build steps - THIS runs in the worker."""
        # Calls from here should use direct worker methods or simple function calls

        if not self._check_kolbanidze_key(): # Uses direct worker call internally now
            if self.build_failed_flag: return False # Check if previous step failed
            if not self._add_kolbanidze_key(): # Uses direct worker call internally now
                return False # Error reported by _add_kolbanidze_key

        if update_apps:
            if not self._update_offline_apps(): return False # Uses direct calls internally now
            if self.build_failed_flag: return False

        if update_repo:
            if not self._update_offline_repo(): return False # Uses direct calls internally now
            if self.build_failed_flag: return False

        if online_build:
            self.log(f"[INFO] === Online {self.lang.build_started} {self.lang.started} ===")
            if not self._cleanup_build_dir(): return False # Uses direct calls internally now
            if self.build_failed_flag: return False
            if not self._build_iso(offline=False): return False # Uses direct calls internally now
            if self.build_failed_flag: return False
            self.log(f"[INFO] === Online {self.lang.build_started} {self.lang.succeed} ===")

        if offline_build:
            self.log(f"[INFO] === Offline {self.lang.build_started} {self.lang.started} ===")
            # Check repo existence directly (worker context)
            if not update_repo and not self._worker_check_offline_repo_files_exist(): # New direct worker check
                 self.log(f"[WARNING] {self.lang.offline_repo_autocreate}", level="warning")
                 if not self._update_offline_repo(): return False # Uses direct calls internally now
                 if self.build_failed_flag: return False

            if not self._cleanup_build_dir(): return False # Uses direct calls internally now
            if self.build_failed_flag: return False
            if not self._build_iso(offline=True): return False # Uses direct calls internally now
            if self.build_failed_flag: return False
            self.log(f"[INFO] === Offline {self.lang.build_started} {self.lang.succeed} ===")
        self._build_success()
        return not self.build_failed_flag # Return True if no failures occurred

    def _build_success(self):
        Notification(self.lang.build_complete_success, title=self.lang.success, icon="greencheck.png", app_instance=self)
        return True


    def _update_offline_apps(self) -> bool:
        """Clones/updates apps. Uses direct worker calls."""
        apps_to_update = {
            "secux-installer": Path(WORKDIR) / "releng/airootfs/usr/local/share/secux-installer",
            "secux-apps": Path(WORKDIR) / "releng/airootfs/usr/local/share/secux-apps",
            "KIRTapp": Path(WORKDIR) / "releng/airootfs/usr/local/share/KIRTapp",
        }

        for name, target_dir in apps_to_update.items():
            repo_url = self.repos.get(name)
            if not repo_url: continue

            self.log(f"[INFO] {self.lang.cloning} {name} -> {target_dir}")

            # Use direct worker file ops
            rm_success = self._worker_safe_rmtree(str(target_dir))
            if not rm_success:
                 self.report_error(f"{self.lang.failed_to_remove} {name} <-> {target_dir}.", show_notification=False)
                 return False
            
            # Use direct worker command execution
            clone_cmd = ["/usr/bin/git", "clone", '--depth=1', repo_url, str(target_dir)]
            result = self._run_command_in_worker(clone_cmd, None, False)
            if result != 0:
                self.report_error(f"{self.lang.clone_failed} {name} ({self.lang.exit_code}: {result}).", show_notification=False)
                return False

        self.log(f"[INFO] {self.lang.offline_apps_update_success}.")
        return True

    # Add this new helper function
    def _worker_check_offline_repo_files_exist(self) -> bool:
        """Directly checks if essential offline repo files exist (for worker thread)."""
        db_path = Path(OFFLINE_REPO_PATH) / "offline-repo.db.tar.zst"
        files_path = Path(OFFLINE_REPO_PATH) / "offline-repo.files.tar.zst"
        exists = db_path.is_file() and files_path.is_file()
        return exists

    def _update_offline_repo(self) -> bool:
        """Downloads packages and creates repo DB. Uses direct worker calls."""
        self.log(f"[INFO] {self.lang.updating_offline_repo} ({OFFLINE_REPO_PATH})")

        self._worker_safe_rmtree(OFFLINE_REPO_PATH)

        # Use direct worker file op
        mk_success = self._worker_safe_mkdir(OFFLINE_REPO_PATH)
        if not mk_success:
             self.report_error(f"{self.lang.offline_repo_fail}: {OFFLINE_REPO_PATH}.", show_notification=False)
             return False

        # Use direct worker command execution for pacman
        pacman_cmd = ["/usr/bin/stdbuf", '-oL', "/usr/bin/pacman", '-Sywu', '--noconfirm',
                      '--cachedir', OFFLINE_REPO_PATH] + PACKAGES
        result = self._run_command_in_worker(pacman_cmd, None, False)
        if result != 0:
             self.report_error(f"{self.lang.update_repo_failed} ({result}).", show_notification=False)
             return False

        self.log(f"[INFO] {self.lang.creating_repo_db}")
        repo_db_path = Path(OFFLINE_REPO_PATH) / "offline-repo.db.tar.zst"
        repo_files_path = Path(OFFLINE_REPO_PATH) / "offline-repo.files.tar.zst"
        repo_path = Path(OFFLINE_REPO_PATH)

        # Direct file system access within worker thread
        files_to_add = []
        try:
            for item in repo_path.iterdir():
                 if item.is_file() and item.name.endswith(('.pkg.tar.zst', '.pkg.tar.xz', '.pkg.tar.gz')) and not item.name.endswith('.sig') and item != repo_db_path and item != repo_files_path:
                      files_to_add.append(str(item))
        except OSError as e:
             self.report_error(f"{self.lang.error_reading_offline_cache} {OFFLINE_REPO_PATH}: {e}", show_notification=False)
             return False
        if not files_to_add:
             self.report_error(f"{self.lang.no_pkgs_found} {OFFLINE_REPO_PATH}.", show_notification=False)
             return False

        # Use direct worker command execution for repo-add
        repo_add_cmd = ['/usr/bin/repo-add', str(repo_db_path)] + files_to_add
        result = self._run_command_in_worker(repo_add_cmd, None, False)
        if result != 0:
             self.report_error(f"{self.lang.create_repo_db_failed} ({result}).", show_notification=False)
             return False

        self.log(f"[INFO] {self.lang.offline_apps_update_success}.")
        return True

    def _cleanup_build_dir(self) -> bool:
        """Cleans build dir. Uses direct worker calls."""
        self.log(f"[INFO] {self.lang.cleaning_dir} {self.bin_dir}")
        # Direct calls to worker-safe functions
        rm_success = self._worker_safe_rmtree(self.bin_dir)
        if not rm_success:
            self.report_error(f"{self.lang.clean_dir_fail_rm} {self.bin_dir}. {self.lang.check_console_log}", show_notification=False)
            return False
        mk_success = self._worker_safe_mkdir(self.bin_dir)
        if not mk_success:
            self.report_error(f"{self.lang.clean_dir_fail_mk} {self.bin_dir}. {self.lang.check_console_log}", show_notification=False)
            return False

        self.log(f"[INFO] {self.lang.clean_dir_ok} {self.bin_dir}")
        return True


    def _build_iso(self, offline: bool) -> bool:
        """Prepares build env and runs mkarchiso. Uses direct worker calls."""
        build_type = "offline" if offline else "online"
        self.log(f"[INFO] {self.lang.preparing_iso} {build_type}")

        # Define paths (direct access is okay in worker)
        airootfs_path = Path(WORKDIR) / "releng/airootfs"
        build_cache_path = airootfs_path / "var/cache/pacman"
        build_offline_repo_cache_path = build_cache_path / "offline-repo"
        installer_path = airootfs_path / "usr/local/share/secux-installer"
        apps_path = airootfs_path / "usr/local/share/secux-apps"
        kirt_path = airootfs_path / "usr/local/share/KIRTapp"
        python_packages_path = installer_path / "python_packages"
        offline_marker_file = installer_path / "offline_installation.conf"

        # Use direct worker file ops
        if not self._worker_safe_mkdir(str(build_cache_path)): return False

        # Check installer presence directly
        if not installer_path.is_dir() or not list(installer_path.iterdir()):
             # Call the _update_offline_apps which now uses direct worker calls
             if not self._update_offline_apps():
                 self.report_error(self.lang.secux_installer_clone_failed, show_notification=False)
                 return False
             if self.build_failed_flag: return False # Check flag again

        # Handle offline/online specific files/dirs using direct calls
        if offline:
            # Check apps presence directly
            if not apps_path.is_dir() or not list(apps_path.iterdir()):
                 if not self._update_offline_apps(): return False
                 if self.build_failed_flag: return False
            if not kirt_path.is_dir() or not list(kirt_path.iterdir()):
                 if not self._update_offline_apps(): return False
                 if self.build_failed_flag: return False

            if not self._worker_create_empty_file(str(offline_marker_file)): return False

            self.log(f"[INFO] {self.lang.copying_offline_cache}")
            if not self._worker_check_offline_repo_files_exist(): # Use direct check
                 self.report_error(f"{self.lang.offline_repo_miss} ({OFFLINE_REPO_PATH})", show_notification=True)
                 return False
            if not self._worker_safe_rmtree(str(build_offline_repo_cache_path)): return False
            if not self._worker_safe_mkdir(str(build_offline_repo_cache_path)): return False
            rsync_cmd = ['/usr/bin/rsync', '-aAXHv', '--delete', str(Path(OFFLINE_REPO_PATH)) + "/", str(build_offline_repo_cache_path)]
            result = self._run_command_in_worker(rsync_cmd, None, False) # Direct worker command
            if result != 0:
                 self.report_error(f"{self.lang.copy_offline_cache_failed} ({result}).", show_notification=False)
                 return False

            self.log(f"[INFO] {self.lang.collecting_py_packages}")
            collect_script = installer_path / "collect_python_packages.sh"
            if not collect_script.exists(): # Direct check
                 self.report_error(f"{self.lang.py_collector_script_miss}: {collect_script}", show_notification=False)
                 return False
            if not self._worker_safe_chmod(str(collect_script), 0o755): return False
            if not self._worker_safe_mkdir(str(python_packages_path)): return False
            result = self._run_command_in_worker(['/usr/bin/bash', str(collect_script), str(python_packages_path)], None, False) # Direct worker command
            if result != 0:
                 self.report_error(f"{self.lang.collect_py_fail} ({result}).", show_notification=False)
                 return False
        else: # Online build cleanup
            if not self._worker_safe_rmtree(str(apps_path)): return False
            if not self._worker_safe_rmtree(str(kirt_path)): return False
            if not self._worker_safe_remove(str(offline_marker_file)): return False
            if not self._worker_safe_rmtree(str(build_offline_repo_cache_path)): return False
            if not self._worker_safe_rmtree(str(python_packages_path)): return False

        # Configure pacman.conf using direct calls
        self.log(f"[INFO] {self.lang.configuring_pacman} {build_type}")
        pacman_conf_src = airootfs_path / f"etc/pacman_{build_type}.conf"
        pacman_conf_dst = airootfs_path / "etc/pacman.conf"
        if not pacman_conf_src.exists(): # Direct check
             self.report_error(f"{self.lang.pacman_config_not_found}: {pacman_conf_src}", show_notification=False)
             return False
        if not self._worker_safe_copy(str(pacman_conf_src), str(pacman_conf_dst)):
             self.report_error(self.lang.configure_pacman_failed, show_notification=False)
             return False

        # Run mkarchiso using direct worker call
        releng_path = Path(WORKDIR) / "releng"
        if not releng_path.is_dir(): # Direct check
             self.report_error(self.lang.releng_error, show_notification=False)
             return False
        mkarchiso_cmd = ["/usr/bin/mkarchiso", '-v', '-w', self.bin_dir, '-o', self.bin_dir, str(releng_path)]
        result = self._run_command_in_worker(mkarchiso_cmd, None, False) # Direct worker command
        if result != 0:
             self.report_error(result, show_notification=True)
             return False

        # Move and rename ISO using direct calls
        default_iso_name = 'Secux-Linux-x86_64.iso'
        src_iso_path = Path(self.bin_dir) / default_iso_name
        if not src_iso_path.exists(): # Direct check
            self.report_error(f"{self.lang.iso_not_found} {src_iso_path}.", show_notification=True)
            return False
        timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M')
        final_iso_name = f"SecuxLinux-{build_type}-{timestamp}.iso"
        dst_iso_path = Path(self.output_dir) / final_iso_name
        if not self._worker_safe_mkdir(str(self.output_dir)): return False
        if not self._worker_safe_move(str(src_iso_path), str(dst_iso_path)):
            self.report_error(f"{self.lang.failed_to_move} {src_iso_path} -> {dst_iso_path}.", show_notification=False)
            return False

        self.log(f"[SUCCESS] {build_type} {self.lang.iso_build_success}: {dst_iso_path}")
        return True

    # --- Worker Thread and Execution Logic ---

    def _worker_loop(self):
        """The loop run by the background worker thread."""
        while not self._stop_worker.is_set():
            task = None
            try:
                task = self.task_queue.get(timeout=0.5) # Timeout to allow checking _stop_worker
                if task is None: # Sentinel for stopping the thread
                    break

                task_type, task_data, completion_event = task
                result = None
                exception = None
                self._current_task_result = None
                self._current_task_exception = None

                try:
                    if task_type == 'execute':
                        command, input_str, suppress_output = task_data
                        result = self._run_command_in_worker(command, input_str, suppress_output)
                    elif task_type == 'execute_function':
                        func, args, kwargs = task_data
                        result = self._run_function_in_worker(func, args, kwargs)
                    else:
                        raise ValueError(f"{self.lang.unknown_task}: {task_type}")

                except Exception as e:
                    # Capture any exception during task execution *itself*
                    exception = e
                    self.log(f"✘ {self.lang.unexpected_error} ({task_type}): {e}\n{traceback.format_exc()}", level="error")
                    # Mark build as failed if an unexpected error occurs during a task
                    self.build_failed_flag = True
                    # Ensure result indicates failure if needed (e.g., return code for command)
                    if task_type == 'execute':
                        result = -2 # General error code

                finally:
                    # Store result and signal completion *regardless* of success/failure
                    self._current_task_result = result
                    self._current_task_exception = exception
                    if completion_event:
                        completion_event.set() # Signal the waiting main thread
                    self.task_queue.task_done() # Mark task as completed in the queue

            except queue.Empty:
                # Queue was empty, loop again to check stop signal
                continue
            except Exception as e:
                 # Handle errors in the worker loop itself (e.g., queue issues)
                 # Use print as self.log might fail if GUI is involved
                 print(f"[ERROR]: {e}\n{traceback.format_exc()}", file=sys.stderr)
                 self.build_failed_flag = True # Mark failure
                 self._stop_worker.set() # Try to stop loop


    def _run_command_in_worker(self, command: List[str], input_str: Optional[str], suppress_output: bool) -> int:
        """Executed by the worker thread to run an external command."""
        display_cmd = ' '.join(shlex.quote(str(c)) for c in command)
        if not suppress_output:
             self.log(f"▶ {self.lang.executing_command} {display_cmd}")

        process = None
        return_code = -1 # Default to error

        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE if input_str is not None else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1, # Line buffered
                encoding='utf-8',
                errors='replace' # Handle potential encoding errors in output
            )

            stdout_lines = []
            stderr_lines = []

            # --- Real-time Output Handling (Worker Thread using self.log) ---
            def read_stream(stream, output_list, stream_name):
                """Reads lines from a stream and uses self.log."""
                try:
                    for line in iter(stream.readline, ''):
                        if line:
                            output_list.append(line)
                            if not suppress_output:
                                self.log(line.strip()) # Log stripped line
                        else:
                            break # End of stream
                except Exception as e:
                     self.log(f"{self.lang.error_reading_stream} ({stream_name}): {e}", level="error")
                finally:
                    try: stream.close()
                    except OSError: pass

            # Use threads to read stdout/stderr concurrently to prevent blocking
            stdout_thread = None
            stderr_thread = None

            if process.stdout:
                 stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, stdout_lines, "stdout"), daemon=True)
                 stdout_thread.start()
            if process.stderr:
                 stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, stderr_lines, "stderr"), daemon=True)
                 stderr_thread.start()

            # Handle stdin if provided (after starting output readers)
            if input_str is not None and process.stdin:
                try:
                    process.stdin.write(input_str)
                    process.stdin.close() # Signal end of input
                except OSError as e:
                    self.log(f"✘ {self.lang.error_writing_to_stdin} {e}", level="error")
                    try: process.kill()
                    except OSError: pass
                    process.wait() # Wait after killing
                    self.log(f"✘ {self.lang.command_failed_stdin}", level="error")
                    self.build_failed_flag = True
                    # Join reader threads before returning
                    if stdout_thread: stdout_thread.join(timeout=1)
                    if stderr_thread: stderr_thread.join(timeout=1)
                    return process.returncode if process.returncode is not None else -1

            # Wait for reader threads to finish *before* waiting for the process
            if stdout_thread: stdout_thread.join()
            if stderr_thread: stderr_thread.join()

            # Wait for the process to terminate and get the final return code
            return_code = process.wait()

            # Final status update
            if return_code == 0:
                 if not suppress_output:
                      self.log(f"✔ {self.lang.command_success} {return_code})")
            else:
                 # Error message comes from stderr thread via self.log
                 self.log(f"✘ {self.lang.command_failed} {return_code})", level="error")
                 self.build_failed_flag = True # Mark build as failed on command error

        except FileNotFoundError:
             self.log(f"✘ {self.lang.command_not_found} '{command[0]}'", level="error")
             self.build_failed_flag = True
             return_code = 127 # Standard code for command not found
        except PermissionError:
             self.log(f"✘ {self.lang.perm_denied}: {display_cmd}", level="error")
             self.build_failed_flag = True
             return_code = 126 # Standard code for permission denied
        except Exception as e:
             # Catch other Popen errors or issues
             self.log(f"✘ {self.lang.unexpected_error}: {e}\n{traceback.format_exc()}", level="error")
             self.build_failed_flag = True
             return_code = -2 # General error code
        finally:
             # Ensure process is cleaned up if it's still running
             if process and process.poll() is None:
                 self.log(f"[INFO] {self.lang.terminating_hanging_process}: {display_cmd}")
                 try:
                     process.terminate()
                     process.wait(timeout=1) # Short wait for graceful term
                 except subprocess.TimeoutExpired:
                     process.kill() # Force kill if terminate fails
                     process.wait() # Wait for kill
                 except Exception as kill_e:
                     self.log(f"[WARNING] {self.lang.err_term}: {kill_e}", level="warning")
                 if return_code >= 0: # If not already set to an error code
                     return_code = -3 # Indicate killed process

        return return_code


    def _run_function_in_worker(self, func: Callable[..., Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
        """Executed by the worker thread to run a Python function."""
        func_name = getattr(func, '__name__', repr(func))
        self.log(f"▶ {self.lang.executing_function} {func_name}")

        f_stdout = io.StringIO()
        f_stderr = io.StringIO()
        return_value = None
        success = False

        try:
            # Redirect std streams *within the worker thread* for this function call only
            with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
                return_value = func(*args, **kwargs)
            success = True # If no exception occurred during func call

        except Exception as e:
             # Exception captured by the main worker loop's try/except
             # Log it here for context associated with the function call
             self.log(f"✘ {self.lang.error_during_function_execution} {func_name}: {e}\n{traceback.format_exc()}", level="error")
             self.build_failed_flag = True
             # Exception object is stored in self._current_task_exception by the caller (_worker_loop)

        finally:
            # Get captured output
            stdout_val = f_stdout.getvalue()
            stderr_val = f_stderr.getvalue()
            f_stdout.close()
            f_stderr.close()

            # Display captured output via self.log
            if stdout_val:
                 self.log(stdout_val.strip())
            if stderr_val:
                 self.log(stderr_val.strip(), level="error")

            # Final status update based on whether the function call itself succeeded
            if success:
                 self.log(f"✔ {self.lang.function} '{func_name}' {self.lang.succeed}")
                 # try:
                 #     return_repr = repr(return_value)
                 #     limit = 200
                 #     if len(return_repr) > limit: return_repr = return_repr[:limit] + "..."
                 #     self.log(f"  {self.lang.return_value} {return_repr}")
                 # except Exception as repr_e:
                 #      self.log(f"  ({self.lang.couldnt_return_value}: {repr_e})", level="warning")
            else:
                 # Error message already printed in except block
                 self.log(f"✘ {self.lang.function} '{func_name}' {self.lang.failed}", level="error")
                 self.build_failed_flag = True

        # Return the value (or None if exception) to _worker_loop
        return return_value if success else None


    def execute_function(self, func: Callable[..., Any], args: Tuple[Any, ...] = (), kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Executes a Python function.
        In GUI mode: Schedules for background execution, waits logically.
        In CLI mode: Executes directly and blocks.

        Returns: The function's return value, or None if an exception occurred.
                 Returns None if build has already failed.
        """
        if self.build_failed_flag:
             func_name = getattr(func, '__name__', repr(func))
             self.log(f"[INFO] {self.lang.skipping_bc_failed}: {func_name}")
             return None # Indicate skipped

        if kwargs is None:
            kwargs = {}

        if self.is_cli:
            # --- CLI Execution ---
            return self._run_function_in_worker(func, args, kwargs)
        else:
            # --- GUI Execution (via Worker Thread) ---
            completion_event = threading.Event()
            task_data = (func, args, kwargs)
            task = ('execute_function', task_data, completion_event)

            # Reset result/exception holders
            self._current_task_result = None
            self._current_task_exception = None

            if not self.task_queue or not self.worker_thread or not self.worker_thread.is_alive():
                self.report_error(self.lang.worker_is_sleeping, exit_on_error=True)
                return None # Should exit

            self.task_queue.put(task)

            # Wait for the worker to signal completion, keeping GUI responsive
            while not completion_event.is_set():
                self.update()

            # Task is done, retrieve result
            if self._current_task_exception:
                # Error logged by worker. Function effectively failed.
                return None # Indicate failure
            else:
                # Return the actual result stored by the worker
                return self._current_task_result


    # --- Worker-Safe File/OS Operations ---
    # These functions are designed to be run via execute_function

    def _worker_safe_rmtree(self, path: str) -> bool:
        """Safely remove a directory tree. Returns True on success, False on failure."""
        path_obj = Path(path)
        if not path_obj.exists():
            # self.log(f"[DEBUG] Path does not exist, skipping rmtree: {path}")
            return True # Nothing to remove
        if not path_obj.is_dir():
             self.log(f"{self.lang.rmtree_not_a_dir}: {path}", level="error")
             return False
        try:
            # self.log(f"[DEBUG] Attempting rmtree: {path}")
            rmtree(path)
            # self.log(f"[DEBUG] rmtree successful: {path}")
            return True
        except Exception as e:
            self.log(f"{self.lang.failed_to_remove_dir} {path}: {e}", level="error")
            return False

    def _worker_safe_mkdir(self, path: str) -> bool:
        """Safely create a directory (including parents). Returns True on success, False on failure."""
        try:
            # self.log(f"[DEBUG] Attempting mkdir: {path}")
            Path(path).mkdir(parents=True, exist_ok=True)
            # self.log(f"[DEBUG] mkdir successful: {path}")
            return True
        except Exception as e:
            self.log(f"{self.lang.failed_to_create_dir} {path}: {e}", level="error")
            return False

    def _worker_safe_remove(self, path: str) -> bool:
        """Safely remove a file. Returns True on success or if file doesn't exist, False on error."""
        path_obj = Path(path)
        if not path_obj.exists():
             # self.log(f"[DEBUG] Path does not exist, skipping remove: {path}")
             return True # Nothing to remove
        if not path_obj.is_file():
             self.log(f"{self.lang.cannot_remove_not_a_file}: {path}", level="error")
             return False
        try:
            # self.log(f"[DEBUG] Attempting remove: {path}")
            os.remove(path)
            # self.log(f"[DEBUG] remove successful: {path}")
            return True
        except Exception as e:
            self.log(f"{self.lang.failed_to_remove_file} {path}: {e}", level="error")
            return False

    def _worker_safe_copy(self, src: str, dst: str) -> bool:
        """Safely copy a file. Returns True on success, False on failure."""
        try:
            # self.log(f"[DEBUG] Attempting copy: {src} -> {dst}")
            copy(src, dst)
            # self.log(f"[DEBUG] copy successful: {src} -> {dst}")
            return True
        except Exception as e:
            self.log(f"{self.lang.failed_to_copy} {src} -> {dst}: {e}", level="error")
            return False

    def _worker_safe_move(self, src: str, dst: str) -> bool:
        """Safely move a file or directory. Returns True on success, False on failure."""
        try:
            # self.log(f"[DEBUG] Attempting move: {src} -> {dst}")
            move(src, dst)
            # self.log(f"[DEBUG] move successful: {src} -> {dst}")
            return True
        except Exception as e:
            self.log(f"{self.lang.failed_to_move} {src} -> {dst}: {e}", level="error")
            return False

    def _worker_safe_chmod(self, path: str, mode: int) -> bool:
        """Safely change mode of a file/dir. Returns True on success, False on failure."""
        try:
            # self.log(f"[DEBUG] Attempting chmod {oct(mode)}: {path}")
            Path(path).chmod(mode)
            # self.log(f"[DEBUG] chmod successful: {path}")
            return True
        except Exception as e:
            self.log(f"{self.lang.failed_to_chmod} {path} -> {oct(mode)}: {e}", level="error")
            return False

    def _worker_create_empty_file(self, path: str) -> bool:
        """Safely create an empty file. Returns True on success, False on failure."""
        try:
            # self.log(f"[DEBUG] Attempting create empty file: {path}")
            path_obj = Path(path)
            # Create parent directories if they don't exist
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            # Create/truncate the file
            with open(path_obj, "w") as f:
                pass
            # self.log(f"[DEBUG] Create empty file successful: {path}")
            return True
        except Exception as e:
            self.log(f"{self.lang.failed_to_create_empty_file} {path}: {e}", level="error")
            return False

    def _worker_path_exists(self, path: str) -> bool:
        """Checks if a path exists. Returns True/False."""
        # This is simple enough not to need excessive logging unless debugging
        return Path(path).exists()


# --- Main Execution ---
if __name__ == "__main__":
    args = setup_arg_parser()

    # --- Language Setup ---
    selected_lang = "en" # Default
    if args.russian:
        selected_lang = "ru"
    elif args.russian is False: # Explicitly set to English via --no-russian
         selected_lang = "en"
    elif args.russian is None: # Auto-detect
        try:
            system_locale_str = getlocale()[0]
            if system_locale_str and 'ru' in system_locale_str.lower():
                selected_lang = "ru"
        except Exception:
            pass # Keep default 'en' if locale detection fails

    lang = Locale(selected_lang)

    # --- Handle Special Arguments ---
    if args.version:
        print(VERSION)
        sys.exit(0)

    check_critical_dependencies() # Checks pacman, root

    if args.install_all_dependencies:
        install_dependencies() # Exits after installing

    # --- Check GUI Availability (if not CLI) ---
    if not args.cli and not gui_available:
         print(lang.falling_back_to_cli, file=sys.stderr)
         args.cli = True # Force CLI mode

    # --- Start Application ---
    try:
        app = App(args, lang)
        if not args.cli:
            app.mainloop() # Start GUI event loop
        # CLI mode runs to completion within App._run_cli() called by __init__
    except Exception as main_e:
         print(f"\n--- [ERROR] ---", file=sys.stderr)
         print(f"{lang.unexpected_error_occurred}: {main_e}", file=sys.stderr)
         print(traceback.format_exc(), file=sys.stderr)
         sys.exit(2)