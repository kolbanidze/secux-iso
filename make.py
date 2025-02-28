#!/usr/bin/python3
import os
import sys
from datetime import datetime
import subprocess
from argparse import ArgumentParser, BooleanOptionalAction
try:
    from requests import get
    from requests.exceptions import ConnectionError
except ModuleNotFoundError:
    print("Модуль requests не найден. Для установки используйте: pacman -S python-requests")
    exit(1)
import configparser

VERSION = "0.1.2"
WORKDIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_REPO_PATH = "/var/cache/pacman/offline-repo"
PACKAGES = "xorg-xkbcomp xapian-core libepubgen qt6-location libburn libmm-glib glibc xorg-setxkbmap qt6-webview libtommath kwindowsystem analitza python-jaraco.functools ffmpeg4.4 poppler vtk libdeflate filelight xorg-xvinfo rocs xcb-util-renderutil gnupg gnugo xorg-xmodmap libsoxr kmod gnome-disk-utility audiotube lua gperftools bluez-libs qt5-graphicaleffects kfilemetadata polkit-kde-agent xorg-x11perf libtirpc clang poppler krecorder libxvidcore.so kparts gdbm python-urllib3 xorg-xkbevd libsigc++-3.0 kservice5 abseil-cpp run-parts libblockdev-part libmpcdec malcontent libktorrent lzo mdadm upower liblouis gnome-menus wpa_supplicant curl libcolord kamoso pambase black-hole-solver wireplumber libksysguard cmark intel-ucode kmousetool lcms2 libkgapi libnfnetlink kxmlgui5 qt5-wayland plasma5support poppler-glib python-hyperlink libcloudproviders breeze oxygen libgxps libmysofa.so kwin kweather kalzium kdenlive libksane ntfs-3g libdecor svt-av1 mutter rtkit libxml2 attica5 mlt itinerary gvfs-dnssd archlinux-appstream-data util-linux tzdata gvfs-nfs libxtables.so artikulate libtheora kauth5 gnome-user-docs kde-gtk-config kalm desktop-file-utils colord-gtk4 kidletime graphviz python-ptyprocess libdav1d.so kmenuedit grilo kate kimagemapeditor libass.so polkit-qt6 xorg-xhost ktexttemplate vte4 python-defusedxml libva kdebugsettings libfabric tesseract kio libmnl socat libosinfo plasma-systemmonitor kparts5 vmaf pim-data-exporter kdegraphics-thumbnailers python kalk gdb-common gnome-characters sonnet openpmix cracklib libxinerama libgtop tbb libtevent.so kdepim-runtime libvidstab.so gcc gnulib-l10n apr-util kpmcore raptor libportal-gtk4 diffutils libxdamage onetbb kdf dconf freecell-solver kcmutils5 libxpresent systemd libjson-glib-1.0.so mesa audit polkit libsysprof-capture libpng libplist falkon avogadro-fragments giflib qt5-multimedia util-linux-libs libavif kaccounts-providers libportal libheif kleopatra gnome-control-center sudo mobile-broadband-provider-info kpipewire mpfr xorg-bdftopcf xorg-server-xnest jsoncpp sbc kamera qt6-tools org.freedesktop.secrets libkscreen libcap-ng libdca gcc-libs libical totem libblockdev-crypto tokodon linux-firmware colord-gtk-common poxml libxmu kdesu5 xf86-video-vesa libx265.so systemd kcalutils keyutils libfontenc plasma-welcome libopenmpt libimobiledevice-glue sqlite libcolord numactl gzip librav1e.so sddm qt6-webchannel libshumate kbookmarks startup-notification kdbusaddons5 libtiff signon-ui appstream-qt libphonenumber brotli kirigami-gallery xorg-xbacklight kglobalaccel lm_sensors libogg ktouch kconfigwidgets5 milou wildmidi rubberband libxkbfile kbookmarks5 recastnavigation mime-types kdesdk-kio xorg-xwayland libgdata libexttextcat fuse3 linux-hardened libakonadi libvisio kpty5 shaderc lv2 kalgebra exiv2 python-qtpy ksquares bolt libsoup3 licenses libnewt slang libxi llvm-libs xorg-xev qt5-speech khangman lpsolve ncurses kconfig libwebrtc-audio-processing-1.so solid vim-runtime qt6-declarative klickety argon2 libblockdev-fs kpimtextedit kdav kdnssd gsettings-desktop-schemas ripgrep python-pip fftw libbluray kaddressbook libgdm gnome-app-list libxres libnma-common onevpl imath python-cryptography breeze-gtk libraw ktextaddons avogadrolibs libelf speech-dispatcher sbsigntools iso-codes keditbookmarks libsixel tk gst-editing-services gdb plasma-desktop libmsym audiocd-kio discover apr kservice ki18n5 libxi vulkan-icd-loader kubrick libblockdev-swap xcb-util-cursor liblc3.so sh xorg-docs qt6-virtualkeyboard geoclue bzip2 gnome-color-manager syntax-highlighting5 kholidays libdisplay-info sord gnome-calendar colord srt xorg-fonts-alias-100dpi pango dav1d mbox-importer curl flashrom kcolorscheme qt6-positioning libbluetooth.so apparmor libsbc.so python-gobject media-player-info plasma-activities-stats python-ytmusicapi kigo purpose5 ldb portaudio discount perl-error python-platformdirs phonon-qt6 base folks lame python-certifi gspell imagemagick shim-signed kcontacts pim-sieve-editor libdmtx python-darkdetect plasmatube libdvdnav libassuan gupnp gnome-text-editor libaec mariadb kajongg gsound liburing libxcomposite liblsmash.so pipewire-session-manager kpat libevent libvpx.so kget grep gnome-connections usbmuxd automake liboauth gst-plugin-gtk kdbusaddons qt5-base libvncserver rav1e poppler-qt6 gtk-vnc fuse-common kpkpass mpvqt konversation kpackage libdatrie libxrandr libgirepository kaccounts-integration cauchy knewstuff5 libksba perl markdownpart libsamplerate soundtouch iptables libodfgen xorg-xkbutils ksirk python-jaraco.text debugedit noto-fonts kdeclarative libisl.so qhull python-attrs libx264.so libmm-glib.so mpg123 kdiagram psmisc gnome-online-accounts libnautilus-extension.so kblocks calendarsupport libqxp gnome-session gnome-contacts python-automat libmfx gvfs-gphoto2 libblockdev-nvme pcre volume_key kdiamond xorg-xinput kteatime gnome-software ghostwriter merkuro gwenview qt6-connectivity fontconfig iproute2 glslang qt6-translations libde265 gst-devtools-libs klettres kuserfeedback audiofile osinfo-db libbytesize djvulibre gobject-introspection-runtime mailimporter python-legacy-cgi knavalbattle libao kunitconversion5 syndication5 baloo gst-python xorg-xdriinfo plasma-browser-integration signond openmpi wayland accessibility-inspector python-more-itertools libspectre ksudoku docbook-xml util-linux-libs ksnakeduel knewstuff massif-visualizer hwdata libebur128 incidenceeditor snappy systemd-libs minuet glib2 ffmpeg ksystemlog gc kontrast pipewire-pulse luajit libxdmcp kcodecs5 libxkbcommon verdict kdesdk-thumbnailers kdecoration mpv xorg-mkfontscale gtkmm-4.0 qt5-declarative db5.3 gom plasma-nm libnsl kwallet5 gvfs-smb parted akonadi-contacts m4 kinfocenter alsa-lib linux-lts unzip mkinitcpio-busybox gnome-tweaks lvm2 libnumbertext libwebp sane kgamma libmspub yelp libegl hunspell karchive5 liblrdf xkeyboard-config libgsf ktuberling gpgme efitools kitemviews gvfs-google zeromq gst-plugins-base-libs xdg-desktop-portal-gtk qt5-script python-pygdbmi simple-scan docbook-xsl libxxf86vm kclock libldac libvpx yelp-xsl libkeduvocdocument graphite gsm python-autocommand gsfonts libtasn1 kio-fuse systemd-ukify python-click svt-hevc ocean-sound-theme libxcvt accounts-qml-module gsl libssh libmalcontent gvfs double-conversion libdovi bomber speexdsp gvfs-wsdd wavpack modemmanager-qt iio-sensor-proxy libcdio emoji-font libei plasma-activities kdeclarative5 gdbm futuresql xdg-desktop-portal-kde kitemviews5 xcb-util-wm gnome-weather json-glib base-devel baloo-widgets harfbuzz-icu frameworkintegration libblockdev-mdraid libva.so xorg-sessreg libcanberra-pulse plymouth-kcm librsvg-2.so ocl-icd libfakekey sdl2 kgeography qcoro libportal-gtk3 xorg-fonts-75dpi opus libmwaw juk librest xorg-xcmsdb minizip akonadi xerces-c binutils libstemmer libusb-1.0.so libwebkitgtk-6.0.so kde-cli-tools boost-libs kimageannotator libfdk-aac.so kio-gdrive molequeue libxpm less fuse2 tcl kcodecs aalib threadweaver kgoldrunner kreversi gtest libupnp ksshaskpass gst-plugin-pipewire jasper qt6-quicktimeline libmtp qt6-speech libcbor twolame attr ffmpegthumbs kscreenlocker libnetfilter_conntrack kcmutils webrtc-audio-processing-1 cups-pk-helper libabw kwidgetsaddons5 arianna kshisen gtksourceview5 libmediaart print-manager libice sddm-kcm sonnet5 glibc kdeplasma-addons xorg-xrefresh xorg-xauth libevdev networkmanager libxft systemd-libs cairomm-1.16 sound-theme-freedesktop libgoa kwallet highway ktextwidgets5 gnome-desktop-common xdg-utils ktexteditor xcb-util libxshmfence okular flatpak libgudev loupe libatasmart python-psutil python-cairo kcharselect libsodium botan plasma-vault kdialog jemalloc protobuf-c kplotting autoconf gnome-calculator libkcddb libmatroska libaccounts-qt libftdi ca-certificates-utils libldacBT_enc.so avogadro-crystals libxcb gnome-shell libvlc qt5-x11extras aha gnome-keyring libgl mpdecimal xdg-desktop-portal kbackup akonadi-calendar-tools alsa-topology-conf breeze-plymouth evince cervisia gst-plugins-bad-libs libidn2 pacman clucene libraqm p11-kit libbluray.so sdl2_ttf kdeedu-data libmanette python-idna json-c pcre2 xorg-xcursorgen krunner libdc1394 openh264 python-wheel dbus-broker-units qrencode gnome-desktop kruler spirv-tools frei0r-plugins libgme mjpegtools libltdl libcanberra neochat yakuake xorg-xkill netpbm kcachegrind layer-shell-qt python-requests freerdp2 kgraphviewer fakeroot gnome-remote-desktop xorg-xdpyinfo xorg-xlsatoms expat libbs2b cdparanoia sweeper v4l-utils kunitconversion marble xdg-desktop-portal-gnome libdaemon xorg-xmessage akregator at-spi2-core device-mapper gst-plugins-base-libs libblockdev kimap python-jaraco.context md4c redland qt6-multimedia kpeople kcrash libqrtr-glib leptonica amd-ucode gpm kdsoap-ws-discovery-client udisks2 dbus libunibreak pulse-native-provider sed graphene kio-admin qt6-httpserver kjournald gnome-music wayland-utils libzip libzimg.so gcr libxv elisa spglib rasqal kolourpaint kontact acl liborcus xcb-util-image libdbusmenu-qt5 mesa-utils kmines libdvdread kompare gtksourceview4 gsettings-system-schemas hdf5 plasma-workspace-wallpapers libkcompactdisc libpipeline libnotify kpackage5 libavcodec.so xorg-xwininfo vid.stab libunistring spectacle librsvg libcue kded5 kasts pinentry kquickimageeditor tecla qt5-quickcontrols libxcrypt ppp qt6-webengine kmahjongg kcompletion5 xorg-xset kde-dev-scripts ddcutil messagelib kded liblangtag a52dec kmailtransport kglobalacceld net-snmp geocode-glib-2 libwnck3 syndication skanlite gnome-backgrounds confuse kongress pahole libgravatar libcdio-paranoia e2fsprogs ktimer python-pefile nettle mariadb-libs xorg-server-xvfb ostree xorg-xsetroot tesseract-data-osd libpaper kmag gtk4 gnome-clocks i2c-tools gupnp-av libnvme fmt kldap systemsettings grantlee-editor speex attica python-filelock kbruch tslib smartmontools kblackbox libmng gnome-user-share libgirepository libcmis gts gupnp-igd libnghttp2 glib-networking kstatusnotifieritem snapshot libcap id3lib kconfigwidgets xorgproto pciutils libfreeaptx python-zope-interface liblilv-0.so libkdepim libpipewire akonadi-mime kmouth awk avogadro-molecules lmdb libkolabxml libplasma kontactinterface xorg-smproxy libkomparediff2 libmd python-constantly apache libatomic_ops ebook-tools libarchive zxing-cpp ufw libfreeaptx.so kjobwidgets wsdd karchive gst-plugins-base opencore-amr krb5 gssdp perl-mailtools orc signon-plugin-oauth2 plasma-workspace libdvbpsi nautilus ttf-hack libmusicbrainz5 kfind efivar ttf-font groff xorg-xlsclients device-mapper dmidecode alsa-card-profiles python-incremental libimobiledevice xxhash man vulkan-tools kcalendarcore bluez-qt xorg-xgamma kdegraphics-mobipocket neon xorg-fonts-100dpi pipewire jbigkit grilo-plugins xorg-xrandr cron libolm libwireplumber libdrm openexr samba gnupg kdepim-addons kbd qca-qt5 linux-api-headers gstreamer iana-etc liblc3 python-dotenv smbclient ktrip libibus ktorrent mariadb-clients kidentitymanagement libe-book hicolor-icon-theme imlib2 libusb libaccounts-glib akonadi-import-wizard solid5 libkdcraw python-pexpect webkit2gtk-4.1 skladnik xorg-xprop korganizer libxmlb openbabel kiconthemes qt5-svg lskat opencv zvbi texinfo zix patch libwbclient kirigami knotifications5 libwpd libwacom baobab libyuv lapack libkexiv2 python-twisted gstreamer kquickcharts icu ca-certificates libzmf kollision libnma-gtk4 qt6-shadertools gvfs-onedrive kio-zeroconf libgexiv2 xdg-dbus-proxy grantleetheme x264 rtmpdump svgpart default-cursors grantlee rygel libqmi cantor gvfs-afc openssh msgraph kcalc libinput qt6-networkauth kplotting5 libmpc fribidi qt6-charts libfreehand libxrender koko kmime telly-skout kmix git palapeli epiphany qt6-websockets gst-plugins-bad gnutls xorg-server-xephyr qgpgme-qt6 webkitgtk-6.0 xorg-xrdb kinit libteam libusbmuxd kopeninghours kcachegrind-common mailcommon pimcommon gsettings-system-schemas libyaml libnice totem-pl-parser libxkbcommon-x11 filesystem kwayland kio5 bash libxss kpublictransport knotifications signon-kwallet-extension libxcursor xmlsec tdb jbig2dec qt5-translations pulseaudio-qt xorg-server kxmlgui xvidcore libgphoto2 kitemmodels ripgrep-all qt6-multimedia-gstreamer llvm khealthcertificate libsoup gnome-console gtk3 glu pacman-mirrorlist python-numpy kcolorchooser breeze-icons libunwind umbrello kguiaddons5 linux-hardened-headers bluez libldap step prrte granatier kwalletmanager cifs-utils nss gnome-logs kosmindoormap xcb-util-keysyms prison kde-inotify-survey libgee python-setuptools libcrypt.so faad2 sbctl knights sratom maeparser openvpn orca polkit-qt5 xdg-user-dirs-gtk qt5-quickcontrols2 plasma-pa kig qt6-quick3d xorg-fonts-alias-75dpi krfb libpcap libiec61883 libp11-kit qt6-5compat ktexteditor5 libxfixes libcups yt-dlp libmicrodns ttf-liberation gnome-keybindings mokutil linux-firmware-whence libpipewire-0.3.so libquotient geocode-glib-common linux-lts-headers libndp openal libreoffice libglvnd kdevelop harfbuzz tar flex gst-plugins-good lokalize libxaw gnome-font-viewer gnome-maps calligra fluidsynth clinfo aribb24 tpm2-tss perl-timedate ghostscript python-pyxdg gnome-bluetooth-3.0 libixion libjcat hunspell tessdata pcsclite gnome-settings-daemon guile phonon-qt6-backend libstaroffice libseccomp ark which thin-provisioning-tools freerdp librevenge bluedevil purpose ksanecore konqueror evolution-data-server spandsp dotconf mujs dolphin mimetreeparser xz qt6-multimedia-backend gd kdoctools parley vulkan-headers openucx libidn knetwalk libpgm sushi glycin findutils kcoreaddons5 pangomm-2.48 katomic freetype2 libverto-module-base khelpcenter fwupd-efi libxtst mod_dnssd kitinerary libjxl libsynctex talloc systemd-sysvcompat libssh2 leancrypto qqc2-breeze-style jack avogadrolibs-qt5 libspelling kactivitymanagerd qqc2-desktop-style kdesu xsettingsd libdbus-1.so gst-plugin-gtk4 libetonyek pipewire-audio kwordquiz francis picmi coreutils libxt qt6-svg gupnp-dlna convertlit kspaceduel kapptemplate lilv zanshin libiptcdata woff2 libx11 killbots compiler-rt akonadiconsole pkgconf kmail libjpeg-turbo iputils npth keepassxc syntax-highlighting libass bovo libksieve python-jaraco.collections kmail-account-wizard libthai libmbim k3b kwave konsole smbclient uchardet readline kauth localsearch plasma-firewall kpty kjumpingcube kscreen gst-plugins-bad-libs gjs kiconthemes5 cfitsio ktnef alligator pam knotifyconfig kcoreaddons libxext colord-sane kanagram networkmanager-qt qt6-base libbsd taglib kcolorpicker libsndfile xf86-input-libinput xorg-server-devel libspeechd shadow libasyncns editorconfig-core-c modemmanager libutempter kqtquickcharts enchant libkdegames xcb-proto kolf libnl kalarm neon gvfs dragon ca-certificates-mozilla angelfish konquest libshout kguiaddons libkleo libnm python-cffi libsystemd.so blas vlc linux-headers xorg-server-common xorg-iceauth adobe-source-code-pro-fonts libaio brltty bubblewrap drkonqi firefox kirigami-addons make kbreakout akonadi-calendar cryptsetup duktape ijs skanpage kglobalaccel5 cairo plasma-sdk kapman gdm libsrtp libnfs tracker3 freeglut gdk-pixbuf2 krdp zbar adwaita-cursors kio-extras kirigami2 python-setproctitle gnome-shell-extensions cantarell-fonts audex libdmapsharing xorg-font-util ksvg plasma-thunderbolt kwallet-pam jansson kiriki libpolkit-gobject-1.so libblockdev-loop kconfig5 aom vapoursynth kbounce qca-qt6 libtool gmp gnome-autoar gvfs-goa gvfs-goa zlib nspr python-dlib shared-mime-info pugixml archlinux-keyring qtkeychain-qt6 initramfs flac kgpg hyphen libmpfr.so qt6-python-bindings openxr protobuf sdl3 re2 libffi plasma-integration colord-kde libxfont2 akonadi-search vte-common kwindowsystem5 libgcrypt kiten dbus-units kturtle libedit pixman libmaxminddb vim ktextwidgets python-typing_extensions libxau python-packaging libproxy xdg-user-dirs gnome-desktop-4 composefs blinken partitionmanager popt kweathercore adwaita-icon-theme avahi opencl-icd-loader kjobwidgets5 python-pycparser libmad liblqr qt6-scxml libcaca libraw1394 libb2 xorg-xwud zstd ksystemstats gnome-system-monitor libavc1394 alsa-ucm-conf libplacebo libebml.so libhandy libpwquality libpagemaker colord keysmith x265 kcrash5 libnghttp3 qt6-wayland xorg-xpr libavtp dbus-broker libwps libpsl python-opencv qt6-imageformats python-dbus python-sentry_sdk dolphin-plugins oxygen-sounds libgoa libxxhash.so libqalculate libmpeg2 flatpak-kcm smbclient plasma-disks linux libltc kcron libgpg-error libinstpatch libcdr hidapi networkmanager-openvpn libnftnl gvfs-mtp accountsservice coordgen xorg-util-macros kmplot libtar kfourinline gettext shiboken6 adwaita-icon-theme-legacy powerdevil kwidgetsaddons kdsoap-qt6 openjpeg2 libp11-kit kdevelop-php libedataserverui4 libfdk-aac source-highlight libexif xorg-fonts-encodings kdeconnect qt6-sensors nano passim exempi python-charset-normalizer kunifiedpush chromaprint poppler-data libgusb kcompletion kde-dev-utils libsasl kwrited file openssl gawk eventviews wacomtablet gcr-4 faac bison glew procps-ng libxslt libvorbis libinih kdenetwork-filesharing pkcs11-helper serd python-pillow libgweather-4 libkmahjongg libsm kmbox xf86-input-wacom gnome-tour libadwaita appstream glibmm-2.68 totem-plparser libvdpau libimagequant binutils chromium isoimagewriter libepoxy marble-common cblas tinysparql plymouth libsecret fwupd ksmtp lz4 libpulse js128 mtdev libpciaccess gtk-update-icon-cache efibootmgr ki18n libmodplug libdv qt5-xmlpatterns kdevelop-python xorg-xwd krdc libieee1284 hwloc klines libqaccessibilityclient-qt6 libpeas libbpf xorg gnome plasma"

parser = ArgumentParser(prog="Secux ISO Builder", description="Программа для сборки ISO образа дистрибутива Secux Linux")
parser.add_argument('-n', '--online', help="создать офлайн сборку (включено по умолчанию)", action=BooleanOptionalAction)
parser.add_argument('-f', '--offline', help="создать онлайн сборку (включено по умолчанию)", action=BooleanOptionalAction)
parser.add_argument('-b', '--bin', help="рабочая папка для сборки", default="bin")
parser.add_argument('-o', '--output', help="папка для ISO образов", default="builds")
#parser.add_argument('-r', '--offline-repo', help="путь до офлайн репозитория", default="/var/cache/pacman/offline-repo")
parser.add_argument('-u', '--update-offline', help="обновить офлайн репозиторий и ПО", action="store_true", default=False)
parser.add_argument('-q', '--quiet', help="не показывать отладочную информацию", action='store_true', default=False)
parser.add_argument('--version', help="показать версию и выйти", action="store_true", default=False)
parser.add_argument('--install-all-dependencies', action='store_true', default=False)
args = parser.parse_args()

# проверить если офлайн репо будет не offline-repo

class Builder:
    def __init__(self, args) -> None:
        self.args = args
        self.repos = {
            "secux-installer": "https://github.com/kolbanidze/secux-installer.git",
            "secux-apps": "https://github.com/kolbanidze/secux-apps.git",
            "KIRTapp": "https://github.com/kirt-king/test_app.git"
            }
                
        if not self.args.quiet:
            print(f"Информация о запуске:\n\tСоздание онлайн сборки: {self.args.online}\n\tСоздание офлайн сборки: {self.args.offline}\n\t"\
                  f"Рабочая папка для сборки: {self.args.bin}\n\tПапка для ISO образов: {self.args.output}\n\t"\
                  f"Обновить офлайн репозиторий: {self.args.update_offline}")
        
        if not self._check_if_arch_based():
            print("[ERROR] Для сброки Secux Linux необходим Arch Linux.")
            exit(1)
        if not self._check_internet_connection():
            print("[ERROR] Для сборки Secux Linux необходимо стабильное подключеие к интернету.")
            exit(1)

        if not os.path.isdir(f"{WORKDIR}/releng"):
            print(f"[ERROR] Директория releng не найдена. Создание образа Secux Linux невозможно.")
            exit(1)
        
        if self.args.install_all_dependencies:
            self._install_all_dependencies()
        self._check_dependencies()

        if not os.path.isdir(self.args.bin):
            print("Создаю папку для сборки.")
            self._execute(f"/usr/bin/mkdir -p {self.args.bin}")
        if not os.path.isdir(self.args.output):
            print("Создаю папку для ISO образов.")
            self._execute(f"/usr/bin/mkdir -p {self.args.output}")

        if self.args.offline:
            if not self._check_offline_repo(OFFLINE_REPO_PATH):
                print(f"[ERROR] Для сборки офлайн образа Secux Linux необходим офлайн репозиторий.")
                exit(1)
        
        if self.args.update_offline:
            for repo, url in self.repos.items():
                if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/{repo}"):
                    os.system(f"/usr/bin/rm -rf {WORKDIR}/releng/airootfs/usr/local/share/{repo}")
                self._execute(f"/usr/bin/git clone --depth=1 {url} {WORKDIR}/releng/airootfs/usr/local/share/{repo}")
            self._update_offline_repo(OFFLINE_REPO_PATH)
            

        if self.args.online:
            self.cleanup()
            self.build(offline = False)
        
        if self.args.offline:
            self.cleanup()
            self.build(offline = True)

    
    def _install_all_dependencies(self):
        self._execute("/usr/bin/pacman -Syu --needed --noconfirm archiso python-pip git bash rsync python-requests", show_what_is_being_executed=True)

    def _execute(self, command: str, show_what_is_being_executed: bool = False) -> None:
        if show_what_is_being_executed: print(f"Выполняется: {command}")
        process = os.system(command)
        if process != 0:
            print(f"[ERROR] Произошла ошибка в время выполнения команды: {command}.")
            exit(1)

    def _check_if_arch_based(self) -> bool:
        if os.path.isfile("/usr/bin/pacman"):
            return True
        else:
            return False
    
    def _check_dependencies(self) -> None:
        requirements = {
            "/usr/bin/mkarchiso": "archiso",
            "/usr/bin/pip": "python-pip",
            "/usr/bin/git": "git",
            "/usr/bin/bash": "bash",
            "/usr/bin/touch": "coreutils",
            "/usr/bin/rsync": "rsync",
            "/usr/bin/chmod": "coreutils"
        }
        errors = False
        for requirement in requirements.items():
            if not os.path.isfile(requirement[0]):
                print(f"[ERROR] {requirement[0]} не найден. Для установки пакета используйте: pacman -S {requirement[1]}")
                errors = True
        if errors: exit(1)
    
    def _check_internet_connection(self) -> bool:
        try:
            answ = get("http://gstatic.com/generate_204", timeout=5)
        except ConnectionError:
            return False
        if answ.status_code != 204:
            return False
        return True

    def _check_offline_repo(self, repo: str) -> bool:
        db_path = os.path.join(repo, "offline-repo.db")
        if os.path.isfile(db_path):
            return True
        else:
            return False

    def _update_offline_repo(self, repo: str) -> bool:
        if os.path.isdir(repo):
            self._execute(f"/usr/bin/rm -rf {repo}")
        self._execute(f"/usr/bin/mkdir -p {repo}")

        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read("/etc/pacman.conf")
        if "kolbanidze" not in parser.sections():
            print("[ERROR] Репозиторий kolbanidze не найден в /etc/pacman.conf. Добавление репозитория.")
            with open("/etc/pacman.conf", "a") as file:
                file.write(f"[kolbanidze]\nServer = https://kolbanidze.github.io/secux-repo/x86_64/\n") 
        
        self._execute(f"/usr/bin/pacman -Sywu --noconfirm --cachedir {repo} {PACKAGES}")
        os.chdir(repo)
        self._execute(f"/usr/bin/repo-add ./offline-repo.db.tar.zst ./*[^sig]")

    def cleanup(self) -> None:
        # Bin/
        if os.path.isdir(self.args.bin):
            self._execute(f"/usr/bin/rm -rf {self.args.bin}")
        else:
            self._execute(f"/usr/bin/mkdir -p {self.args.bin}")
        
        # Builds/
        if not os.path.isdir(self.args.output):
            self._execute(f"/usr/bin/mkdir -p {self.args.output}")
        
        # secux-apps secux-installer KIRTapp
        paths_to_remove = [
            "secux-apps",
            "secux-installer",
            "KIRTapp"
        ]
        
        for path in paths_to_remove:
            full_path = f"{WORKDIR}/releng/airootfs/usr/local/share/{path}"
            if os.path.isdir(full_path):
                self._execute(f"/usr/bin/rm -rf {full_path}")
    
    def build(self, offline: bool) -> None:
        self._execute(f"/usr/bin/mkdir -p {WORKDIR}/releng/airootfs/var/cache/pacman")
        
        if not os.path.isfile(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/main.py"):
            print("Secux Installer не найден в releng. Устанавливается последняя версия.")
            if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer"):
                self._execute(f"/usr/bin/rm -rf {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/")
            self._execute(f"/usr/bin/git clone --depth=1 {self.repos['secux-installer']} {WORKDIR}/releng/airootfs/usr/local/share/secux-installer")
        
        if offline:
            if not os.path.isfile(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-apps/manager.py"):
                print("Security Manager не найден в releng. Устанаваливается последняя версия.")
                if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-apps"):
                    self._execute(f"/usr/bin/rm -rf {WORKDIR}/releng/airootfs/usr/local/share/secux-apps")
                self._execute(f"/usr/bin/git clone --depth=1 {self.repos['secux-apps']} {WORKDIR}/releng/airootfs/usr/local/share/secux-apps")

            if not os.path.isfile(f"{WORKDIR}/releng/airootfs/usr/local/share/KIRTapp/app_script/app.py"):
                print("KIRTapp не найден в releng. Устанавливается последняя версия.")
                if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/KIRTapp"):
                    self._execute(f"/usr/bin/rm -rf {WORKDIR}/releng/airootfs/usr/local/share/KIRTapp")

                self._execute(f"/usr/bin/git clone --depth=1 {self.repos['KIRTapp']} {WORKDIR}/releng/airootfs/usr/local/share/KIRTapp")

        self._execute(f"/usr/bin/touch {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/production.conf")

        if offline:
            if not os.path.isfile(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf"):
                print("Сборка офлайн образа. Создание offline_installation.conf.")
                self._execute(f"/usr/bin/touch {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf")
        else:
            if os.path.isfile(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf"):
                print("Сборка онлайн образа. Удаление offline_installation.conf.")
                os.remove(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf")
        
        if offline:
            self._execute(f"/usr/bin/rm -rf {WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo")
            print("Сборка офлайн образа. Копирование офлайн репозитория.")
            self._execute(f"/usr/bin/rsync -aAXHv --info=progress2 {OFFLINE_REPO_PATH}/* {WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo/")
        else:
            if os.path.isdir(f"{WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo"):
                if os.listdir(f"{WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo") != 0:
                    print("Сборка онлайн образа. Удаление офлайн репозитория.")
                    self._execute(f"/usr/bin/rm -rf {WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo/*")
            if os.path.isdir(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages"):
                if os.listdir(f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages") != 0:
                    print("Сборка онлайн образа. Удаление python пакетов.")
                    self._execute(f"/usr/bin/rm -rf {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages/*")
        
        if offline:
            self._execute(f"/usr/bin/cp {WORKDIR}/releng/airootfs/etc/pacman_offline.conf {WORKDIR}/releng/airootfs/etc/pacman.conf")
        else:
            self._execute(f"/usr/bin/cp {WORKDIR}/releng/airootfs/etc/pacman_online.conf {WORKDIR}/releng/airootfs/etc/pacman.conf")
        
        if offline:
            self._execute(f"/usr/bin/chmod +x {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/collect_python_packages.sh")
            self._execute(f"/usr/bin/bash {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/collect_python_packages.sh {WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages")

        self._execute(f"/usr/bin/mkarchiso -v -w {self.args.bin} -o {self.args.bin} {WORKDIR}/releng")
        buildtype = "offline" if offline else "online"
        build = f"SecuxLinux-{buildtype}-{datetime.today().strftime('%Y-%m-%d_%H-%M')}.iso"
        self._execute(f"/usr/bin/mv {os.path.join(self.args.bin, '*.iso')} {os.path.join(self.args.output, build)}")
        print("="*32)
        print(f"{buildtype} build: {build} success.")
        print('='*32)


if __name__ == "__main__":
    if args.version:
        print(VERSION)
        exit(0)
    if os.geteuid() != 0:
        print("Пожалуйста, запустите от root пользователя!")
        sys.exit(1)
    Builder(args)
