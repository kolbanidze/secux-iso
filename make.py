import os
import subprocess
from argparse import ArgumentParser, BooleanOptionalAction
import threading
from datetime import datetime

VERSION = "0.2.1"
WORKDIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_REPO_PATH = "/var/cache/pacman/offline-repo"
PACKAGES = "a52dec aalib abseil-cpp accessibility-inspector accounts-qml-module accountsservice acl adobe-source-code-pro-fonts adwaita-cursors adwaita-icon-theme adwaita-icon-theme-legacy aha akonadi akonadi-calendar akonadi-calendar-tools akonadi-contacts akonadi-import-wizard akonadi-mime akonadi-search akonadiconsole akregator alligator alsa-card-profiles alsa-lib alsa-topology-conf alsa-ucm-conf amd-ucode analitza angelfish aom apache apparmor appstream appstream-qt apr apr-util archlinux-appstream-data archlinux-keyring argon2 arianna aribb24 ark artikulate at-spi2-core attica attica5 attr audex audiocd-kio audiofile audiotube audit autoconf automake avahi avogadro-crystals avogadro-fragments avogadro-molecules avogadrolibs avogadrolibs-qt5 awk baloo baloo-widgets baobab base base-devel bash binutils binutils bison black-hole-solver blas blinken bluedevil bluez bluez-libs bluez-qt bolt bomber boost-libs botan bovo breeze breeze-gtk breeze-icons breeze-plymouth brltty brotli bubblewrap bzip2 ca-certificates ca-certificates-mozilla ca-certificates-utils cairo cairomm-1.16 calendarsupport calligra cantarell-fonts cantor cauchy cblas cdparanoia cervisia cfitsio chromaprint chromium cifs-utils clang clinfo clucene cmark colord colord colord-gtk-common colord-gtk4 colord-kde colord-sane compiler-rt composefs confuse convertlit coordgen coreutils cracklib cron cryptsetup cups-pk-helper curl curl dav1d db5.3 dbus dbus-broker dbus-broker-units dbus-units dconf ddcutil debugedit default-cursors desktop-file-utils device-mapper device-mapper diffutils discount discover djvulibre dmidecode docbook-xml docbook-xsl dolphin dolphin-plugins dotconf double-conversion dragon drkonqi duktape e2fsprogs ebook-tools editorconfig-core-c efibootmgr efitools efivar elisa emoji-font enchant epiphany eventviews evince evolution-data-server exempi exiv2 expat faac faad2 fakeroot falkon ffmpeg ffmpeg4.4 ffmpegthumbs fftw file filelight filesystem findutils firefox flac flashrom flatpak flatpak-kcm flex fluidsynth fmt folks fontconfig frameworkintegration francis freecell-solver freeglut freerdp freerdp2 freetype2 frei0r-plugins fribidi fuse-common fuse2 fuse3 futuresql fwupd fwupd-efi gawk gc gcc gcc-libs gcr gcr-4 gd gdb gdb-common gdbm gdbm gdk-pixbuf2 gdm geoclue geocode-glib-2 geocode-glib-common gettext ghostscript ghostwriter giflib git gjs glew glib-networking glib2 glibc glibc glibmm-2.68 glslang glu glycin gmp gnome gnome-app-list gnome-autoar gnome-backgrounds gnome-bluetooth-3.0 gnome-calculator gnome-calendar gnome-characters gnome-clocks gnome-color-manager gnome-connections gnome-console gnome-contacts gnome-control-center gnome-desktop gnome-desktop-4 gnome-desktop-common gnome-disk-utility gnome-font-viewer gnome-keybindings gnome-keyring gnome-logs gnome-maps gnome-menus gnome-music gnome-online-accounts gnome-remote-desktop gnome-session gnome-settings-daemon gnome-shell gnome-shell-extensions gnome-software gnome-system-monitor gnome-text-editor gnome-tour gnome-tweaks gnome-user-docs gnome-user-share gnome-weather gnugo gnulib-l10n gnupg gnupg gnutls gobject-introspection-runtime gom gperftools gpgme gpm granatier grantlee grantlee-editor grantleetheme graphene graphite graphviz grep grilo grilo-plugins groff gsettings-desktop-schemas gsettings-system-schemas gsettings-system-schemas gsfonts gsl gsm gsound gspell gssdp gst-devtools-libs gst-editing-services gst-plugin-gtk gst-plugin-gtk4 gst-plugin-pipewire gst-plugins-bad gst-plugins-bad-libs gst-plugins-bad-libs gst-plugins-base gst-plugins-base-libs gst-plugins-base-libs gst-plugins-good gst-python gstreamer gstreamer gtest gtk-update-icon-cache gtk-vnc gtk3 gtk4 gtkmm-4.0 gtksourceview4 gtksourceview5 gts guile gupnp gupnp-av gupnp-dlna gupnp-igd gvfs gvfs gvfs-afc gvfs-dnssd gvfs-goa gvfs-goa gvfs-google gvfs-gphoto2 gvfs-mtp gvfs-nfs gvfs-onedrive gvfs-smb gvfs-wsdd gwenview gzip harfbuzz harfbuzz-icu hdf5 hicolor-icon-theme hidapi highway hunspell hunspell hwdata hwloc hyphen i2c-tools iana-etc icu id3lib iio-sensor-proxy ijs imagemagick imath imlib2 incidenceeditor initramfs intel-ucode iproute2 iptables iputils iso-codes isoimagewriter itinerary jack jansson jasper jbig2dec jbigkit jemalloc js128 json-c json-glib jsoncpp juk k3b kaccounts-integration kaccounts-providers kactivitymanagerd kaddressbook kajongg kalarm kalgebra kalk kalm kalzium kamera kamoso kanagram kapman kapptemplate karchive karchive5 kasts kate katomic kauth kauth5 kbackup kbd kblackbox kblocks kbookmarks kbookmarks5 kbounce kbreakout kbruch kcachegrind kcachegrind-common kcalc kcalendarcore kcalutils kcharselect kclock kcmutils kcmutils5 kcodecs kcodecs5 kcolorchooser kcolorpicker kcolorscheme kcompletion kcompletion5 kconfig kconfig5 kconfigwidgets kconfigwidgets5 kcontacts kcoreaddons kcoreaddons5 kcrash kcrash5 kcron kdav kdbusaddons kdbusaddons5 kde-cli-tools kde-dev-scripts kde-dev-utils kde-gtk-config kde-inotify-survey kdebugsettings kdeclarative kdeclarative5 kdeconnect kdecoration kded kded5 kdeedu-data kdegraphics-mobipocket kdegraphics-thumbnailers kdenetwork-filesharing kdenlive kdepim-addons kdepim-runtime kdeplasma-addons kdesdk-kio kdesdk-thumbnailers kdesu kdesu5 kdevelop kdevelop-php kdevelop-python kdf kdiagram kdialog kdiamond kdnssd kdoctools kdsoap-qt6 kdsoap-ws-discovery-client keditbookmarks keepassxc keysmith keyutils kfilemetadata kfind kfourinline kgamma kgeography kget kglobalaccel kglobalaccel5 kglobalacceld kgoldrunner kgpg kgraphviewer kguiaddons kguiaddons5 khangman khealthcertificate khelpcenter kholidays ki18n ki18n5 kiconthemes kiconthemes5 kidentitymanagement kidletime kig kigo killbots kimageannotator kimagemapeditor kimap kinfocenter kinit kio kio-admin kio-extras kio-fuse kio-gdrive kio-zeroconf kio5 kirigami kirigami-addons kirigami-gallery kirigami2 kiriki kitemmodels kitemviews kitemviews5 kiten kitinerary kjobwidgets kjobwidgets5 kjournald kjumpingcube kldap kleopatra klettres klickety klines kmag kmahjongg kmail kmail-account-wizard kmailtransport kmbox kmenuedit kmime kmines kmix kmod kmousetool kmouth kmplot knavalbattle knetwalk knewstuff knewstuff5 knights knotifications knotifications5 knotifyconfig koko kolf kollision kolourpaint kompare kongress konqueror konquest konsole kontact kontactinterface kontrast konversation kopeninghours korganizer kosmindoormap kpackage kpackage5 kparts kparts5 kpat kpeople kpimtextedit kpipewire kpkpass kplotting kplotting5 kpmcore kpty kpty5 kpublictransport kqtquickcharts kquickcharts kquickimageeditor krb5 krdc krdp krecorder kreversi krfb kruler krunner ksanecore kscreen kscreenlocker kservice kservice5 kshisen ksirk ksmtp ksnakeduel kspaceduel ksquares ksshaskpass kstatusnotifieritem ksudoku ksvg ksystemlog ksystemstats kteatime ktextaddons ktexteditor ktexteditor5 ktexttemplate ktextwidgets ktextwidgets5 ktimer ktnef ktorrent ktouch ktrip ktuberling kturtle kubrick kunifiedpush kunitconversion kunitconversion5 kuserfeedback kwallet kwallet-pam kwallet5 kwalletmanager kwave kwayland kweather kweathercore kwidgetsaddons kwidgetsaddons5 kwin kwindowsystem kwindowsystem5 kwordquiz kwrited kxmlgui kxmlgui5 lame lapack layer-shell-qt lcms2 ldb leancrypto leptonica less libabw libaccounts-glib libaccounts-qt libadwaita libaec libaio libakonadi libao libarchive libass libass.so libassuan libasyncns libatasmart libatomic_ops libavc1394 libavcodec.so libavif libavtp libb2 libblockdev libblockdev-crypto libblockdev-fs libblockdev-loop libblockdev-mdraid libblockdev-nvme libblockdev-part libblockdev-swap libbluetooth.so libbluray libbluray.so libbpf libbs2b libbsd libburn libbytesize libcaca libcanberra libcanberra-pulse libcap libcap-ng libcbor libcdio libcdio-paranoia libcdr libcloudproviders libcmis libcolord libcolord libcrypt.so libcue libcups libdaemon libdatrie libdav1d.so libdbus-1.so libdbusmenu-qt5 libdc1394 libdca libde265 libdecor libdeflate libdisplay-info libdmapsharing libdmtx libdovi libdrm libdv libdvbpsi libdvdnav libdvdread libe-book libebml.so libebur128 libedataserverui4 libedit libegl libei libelf libepoxy libepubgen libetonyek libevdev libevent libexif libexttextcat libfabric libfakekey libfdk-aac libfdk-aac.so libffi libfontenc libfreeaptx libfreeaptx.so libfreehand libftdi libgcrypt libgdata libgdm libgee libgexiv2 libgirepository libgirepository libgl libglvnd libgme libgoa libgoa libgpg-error libgphoto2 libgravatar libgsf libgtop libgudev libgusb libgweather-4 libgxps libhandy libheif libibus libical libice libidn libidn2 libiec61883 libieee1284 libimagequant libimobiledevice libimobiledevice-glue libinih libinput libinstpatch libiptcdata libisl.so libixion libjcat libjpeg-turbo libjson-glib-1.0.so libjxl libkcddb libkcompactdisc libkdcraw libkdegames libkdepim libkeduvocdocument libkexiv2 libkgapi libkleo libkmahjongg libkolabxml libkomparediff2 libksane libksba libkscreen libksieve libksysguard libktorrent liblangtag liblc3 liblc3.so libldac libldacBT_enc.so libldap liblilv-0.so liblouis liblqr liblrdf liblsmash.so libltc libltdl libmad libmalcontent libmanette libmatroska libmaxminddb libmbim libmd libmediaart libmfx libmicrodns libmm-glib libmm-glib.so libmng libmnl libmodplug libmpc libmpcdec libmpeg2 libmpfr.so libmspub libmsym libmtp libmusicbrainz5 libmwaw libmysofa.so libnautilus-extension.so libndp libnetfilter_conntrack libnewt libnfnetlink libnfs libnftnl libnghttp2 libnghttp3 libnice libnl libnm libnma-common libnma-gtk4 libnotify libnsl libnumbertext libnvme liboauth libodfgen libogg libolm libopenmpt liborcus libosinfo libp11-kit libp11-kit libpagemaker libpaper libpcap libpciaccess libpeas libpgm libphonenumber libpipeline libpipewire libpipewire-0.3.so libplacebo libplasma libplist libpng libpolkit-gobject-1.so libportal libportal-gtk3 libportal-gtk4 libproxy libpsl libpulse libpwquality libqaccessibilityclient-qt6 libqalculate libqmi libqrtr-glib libquotient libqxp libraqm librav1e.so libraw libraw1394 libreoffice librest librevenge librsvg librsvg-2.so libsamplerate libsasl libsbc.so libseccomp libsecret libshout libshumate libsigc++-3.0 libsixel libsm libsndfile libsodium libsoup libsoup3 libsoxr libspectre libspeechd libspelling libsrtp libssh libssh2 libstaroffice libstemmer libsynctex libsysprof-capture libsystemd.so libtar libtasn1 libteam libtevent.so libthai libtheora libtiff libtirpc libtommath libtool libunibreak libunistring libunwind libupnp liburing libusb libusb-1.0.so libusbmuxd libutempter libva libva.so libvdpau libverto-module-base libvidstab.so libvisio libvlc libvncserver libvorbis libvpx libvpx.so libwacom libwbclient libwebkitgtk-6.0.so libwebp libwebrtc-audio-processing-1.so libwireplumber libwnck3 libwpd libwps libx11 libx264.so libx265.so libxau libxaw libxcb libxcomposite libxcrypt libxcursor libxcvt libxdamage libxdmcp libxext libxfixes libxfont2 libxft libxi libxi libxinerama libxkbcommon libxkbcommon-x11 libxkbfile libxml2 libxmlb libxmu libxpm libxpresent libxrandr libxrender libxres libxshmfence libxslt libxss libxt libxtables.so libxtst libxv libxvidcore.so libxxf86vm libxxhash.so libyaml libyuv libzimg.so libzip libzmf licenses lilv linux linux-api-headers linux-firmware linux-firmware-whence linux-hardened linux-hardened-headers linux-headers linux-lts linux-lts-headers llvm llvm-libs lm_sensors lmdb localsearch lokalize loupe lpsolve lskat lua luajit lv2 lvm2 lz4 lzo m4 maeparser mailcommon mailimporter make malcontent man marble marble-common mariadb mariadb-clients mariadb-libs markdownpart massif-visualizer mbox-importer md4c mdadm media-player-info merkuro mesa mesa-utils messagelib milou mime-types mimetreeparser minizip minuet mjpegtools mkinitcpio-busybox mlt mobile-broadband-provider-info mod_dnssd modemmanager modemmanager-qt mokutil molequeue mpdecimal mpfr mpg123 mpv mpvqt msgraph mtdev mujs mutter nano nautilus ncurses neochat neon neon net-snmp netpbm nettle networkmanager networkmanager-openvpn networkmanager-qt noto-fonts npth nspr nss ntfs-3g numactl ocean-sound-theme ocl-icd okular onetbb onevpl openal openbabel opencl-icd-loader opencore-amr opencv openexr openh264 openjpeg2 openmpi openpmix openssh openssl openucx openvpn openxr opus orc orca org.freedesktop.secrets osinfo-db ostree oxygen oxygen-sounds p11-kit pacman pacman-mirrorlist pahole palapeli pam pambase pango pangomm-2.48 parley parted partitionmanager passim patch pciutils pcre pcre2 pcsclite perl perl-error perl-mailtools perl-timedate phonon-qt6 phonon-qt6-backend picmi pim-data-exporter pim-sieve-editor pimcommon pinentry pipewire pipewire-audio pipewire-pulse pipewire-session-manager pixman pkcs11-helper pkgconf plasma plasma-activities plasma-activities-stats plasma-browser-integration plasma-desktop plasma-disks plasma-firewall plasma-integration plasma-nm plasma-pa plasma-sdk plasma-systemmonitor plasma-thunderbolt plasma-vault plasma-welcome plasma-workspace plasma-workspace-wallpapers plasma5support plasmatube plymouth plymouth-kcm polkit polkit-kde-agent polkit-qt5 polkit-qt6 poppler poppler poppler-data poppler-glib poppler-qt6 popt portaudio postgresql-libs powerdevil poxml ppp print-manager prison procps-ng protobuf protobuf-c prrte psmisc pugixml pulse-native-provider pulseaudio-qt purpose purpose5 python python-attrs python-autocommand python-automat python-cairo python-certifi python-cffi python-charset-normalizer python-click python-constantly python-cryptography python-darkdetect python-dbus python-defusedxml python-dlib python-dotenv python-filelock python-gobject python-greenlet python-hyperlink python-idna python-incremental python-jaraco.collections python-jaraco.context python-jaraco.functools python-jaraco.text python-legacy-cgi python-more-itertools python-numpy python-opencv python-packaging python-pefile python-pexpect python-pillow python-pip python-platformdirs python-psutil python-psycopg2 python-ptyprocess python-pycparser python-pygdbmi python-pyxdg python-qtpy python-requests python-sentry_sdk python-setproctitle python-setuptools python-sqlalchemy python-twisted python-typing_extensions python-urllib3 python-wheel python-ytmusicapi python-zope-interface qca-qt5 qca-qt6 qcoro qgpgme-qt6 qhull qqc2-breeze-style qqc2-desktop-style qrencode qt5-base qt5-declarative qt5-graphicaleffects qt5-multimedia qt5-quickcontrols qt5-quickcontrols2 qt5-script qt5-speech qt5-svg qt5-translations qt5-wayland qt5-x11extras qt5-xmlpatterns qt6-5compat qt6-base qt6-charts qt6-connectivity qt6-declarative qt6-httpserver qt6-imageformats qt6-location qt6-multimedia qt6-multimedia-backend qt6-multimedia-gstreamer qt6-networkauth qt6-positioning qt6-python-bindings qt6-quick3d qt6-quicktimeline qt6-scxml qt6-sensors qt6-shadertools qt6-speech qt6-svg qt6-tools qt6-translations qt6-virtualkeyboard qt6-wayland qt6-webchannel qt6-webengine qt6-websockets qt6-webview qtkeychain-qt6 raptor rasqal rav1e re2 readline recastnavigation redland ripgrep ripgrep-all rocs rtkit rtmpdump rubberband run-parts rygel samba sane sbc sbctl sbsigntools sddm sddm-kcm sdl2 sdl2_ttf sdl3 sed serd sh shaderc shadow shared-mime-info shiboken6 shim-signed signon-kwallet-extension signon-plugin-oauth2 signon-ui signond simple-scan skanlite skanpage skladnik slang smartmontools smbclient smbclient smbclient snappy snapshot socat solid solid5 sonnet sonnet5 sord sound-theme-freedesktop soundtouch source-highlight spandsp spectacle speech-dispatcher speex speexdsp spglib spirv-tools sqlite sratom srt startup-notification step sudo sushi svgpart svt-av1 svt-hevc sweeper syndication syndication5 syntax-highlighting syntax-highlighting5 systemd systemd systemd-libs systemd-libs systemd-sysvcompat systemd-ukify systemsettings taglib talloc tar tbb tcl tdb tecla telly-skout tessdata tesseract tesseract-data-osd texinfo thin-provisioning-tools threadweaver tinysparql tk tokodon totem totem-pl-parser totem-plparser tpm2-tss tracker3 tslib ttf-font ttf-hack ttf-liberation twolame tzdata uchardet udisks2 ufw umbrello unzip upower usbmuxd util-linux util-linux-libs util-linux-libs v4l-utils vapoursynth verdict vid.stab vim vim-runtime vlc vmaf volume_key vte-common vte4 vtk vulkan-headers vulkan-icd-loader vulkan-tools wacomtablet wavpack wayland wayland-utils webkit2gtk-4.1 webkitgtk-6.0 webrtc-audio-processing-1 which wildmidi wireplumber woff2 wpa_supplicant wsdd x264 x265 xapian-core xcb-proto xcb-util xcb-util-cursor xcb-util-image xcb-util-keysyms xcb-util-renderutil xcb-util-wm xdg-dbus-proxy xdg-desktop-portal xdg-desktop-portal-gnome xdg-desktop-portal-gtk xdg-desktop-portal-kde xdg-user-dirs xdg-user-dirs-gtk xdg-utils xerces-c xf86-input-libinput xf86-input-wacom xf86-video-vesa xkeyboard-config xmlsec xorg xorg-bdftopcf xorg-docs xorg-font-util xorg-fonts-100dpi xorg-fonts-75dpi xorg-fonts-alias-100dpi xorg-fonts-alias-75dpi xorg-fonts-encodings xorg-iceauth xorg-mkfontscale xorg-server xorg-server-common xorg-server-devel xorg-server-xephyr xorg-server-xnest xorg-server-xvfb xorg-sessreg xorg-setxkbmap xorg-smproxy xorg-util-macros xorg-x11perf xorg-xauth xorg-xbacklight xorg-xcmsdb xorg-xcursorgen xorg-xdpyinfo xorg-xdriinfo xorg-xev xorg-xgamma xorg-xhost xorg-xinput xorg-xkbcomp xorg-xkbevd xorg-xkbutils xorg-xkill xorg-xlsatoms xorg-xlsclients xorg-xmessage xorg-xmodmap xorg-xpr xorg-xprop xorg-xrandr xorg-xrdb xorg-xrefresh xorg-xset xorg-xsetroot xorg-xvinfo xorg-xwayland xorg-xwd xorg-xwininfo xorg-xwud xorgproto xsettingsd xvidcore xxhash xz yakuake yelp yelp-xsl yt-dlp zanshin zbar zeromq zix zlib zstd zvbi zxing-cpp"

parser = ArgumentParser(prog="Secux ISO Builder", description="Программа для сборки ISO образа дистрибутива Secux Linux")
parser.add_argument('-c', '--cli', help="отключить графический режим", action=BooleanOptionalAction, default=False)
parser.add_argument('-n', '--online', help="создать онлайн сборку (включено по умолчанию), требует --cli для эффекта", action=BooleanOptionalAction)
parser.add_argument('-f', '--offline', help="создать офлайн сборку (включено по умолчанию), требует --cli для эффекта", action=BooleanOptionalAction)
parser.add_argument('-b', '--bin', help="рабочая папка для сборки, требует --cli для эффекта", default="bin")
parser.add_argument('-o', '--output', help="папка для ISO образов, требует --cli для эффекта", default="builds")
parser.add_argument('-u', '--update-offline-software', help="обновить офлайн ПО, требует --cli для эффекта", action="store_true", default=False)
parser.add_argument('-i', '--update-offline-repo', help="обновить офлайн репозиторий, требует --cli для эффекта", action="store_true", default=False)
parser.add_argument('-s', '--scaling', help="масштабирование графического интерфейса (в процентах, например: -s 100)", default="100")
parser.add_argument('-d', '--dark-theme', help="использовать темную тему", action='store_true', default=False)
parser.add_argument('--version', help="показать версию и выйти", action="store_true", default=False)
parser.add_argument('--install-all-dependencies', help="установить все зависимости и выйти", action='store_true', default=False)
args = parser.parse_args()

if args.version:
    print(VERSION)
    exit(0)

if args.install_all_dependencies:
    os.system("/usr/bin/pacman -Syu --needed --noconfirm archiso python-pip python-pillow git bash rsync python-requests python-packaging python-darkdetect")
    os.system("/usr/bin/pip install customtkinter --break-system-packages")
    exit(0)

if not os.path.isfile("/usr/bin/pacman"):
    print("[ERROR] Для сброки Secux Linux необходим Arch Linux или основанный на нем дистрибутив")
    exit(1)

error = False
try:
    from customtkinter import *
except ModuleNotFoundError:
    print("[ERROR] CustomTkinter не установлен. Для установки используйте: pip install customtkinter")
    error = True

try:
    from tkinter import filedialog
except ModuleNotFoundError:
    print("[ERROR] Tkinter не установлен. Для установки используйте: pacman -Sy tk")
    error = True

try:
    from requests import get
except ModuleNotFoundError:
    print("[ERROR] Requests не установлен. Для установки используйте: pacman -Sy python-requests")
    error = True

try:
    from PIL import Image
except ModuleNotFoundError:
    print("[ERROR] Pillow не установлен. Для установки используйте: pacman -Sy python-pillow")
    error = True

if error: 
    print("При запуске были обнаружены отсутствующие зависимости. Для автоматической установки используйте флаг: --install-all-dependencies")
    exit(1)

if os.geteuid() != 0:
    print("[ERROR] Запускайте приложение только от суперпользователя!")
    exit(1)

class Notification(CTkToplevel):
    def __init__(self, message: str, title: str = "Ошибка", icon: str = "warning.png", message_bold: bool = False, exit_btn_msg: str = "Выйти"):
        if args.cli:
            return
        super().__init__()
        self.title(title)
        image = CTkImage(light_image=Image.open(f'{WORKDIR}/images/{icon}'), dark_image=Image.open(f'{WORKDIR}/images/{icon}'), size=(80, 80))
        image_label = CTkLabel(self, text="", image=image)
        label = CTkLabel(self, text=message)
        if message_bold:
            label.configure(font=(None, 16, "bold"))
        exit_button = CTkButton(self, text=exit_btn_msg, command=self.destroy)
        self.bind(("<Return>"), lambda event: self.destroy())
        image_label.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")
        label.grid(row=0, column=1, padx=15, pady=5, sticky="nsew")
        exit_button.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")



class App(CTk):
    def __init__(self):
        self.repos = {
            "secux-installer": "https://github.com/kolbanidze/secux-installer.git",
            "secux-apps": "https://github.com/kolbanidze/secux-apps.git",
            "KIRTapp": "https://github.com/kirt-king/test_app.git"
            }
        
        if args.cli:
            print("[INFO] Включен режим командной строки.")
            self.bin = args.bin
            self.output = args.output
            self.commands = []

            if not os.path.isdir(f"{WORKDIR}/releng"):
                print(f"[ERROR] Директория releng не найдена. Создание образа Secux Linux невозможно.")
                return
            
            if not self._check_internet_connection():
                print("[ERROR] Для сборки Secux Linux необходимо стабильное подключеие к интернету.")
                return
            
            if not self._check_dependencies():
                print("[ERROR] Не установлены необходимые зависимости.")
                return

            if args.update_offline_software:
                self.__update_apps()
            if args.update_offline_repo:
                self.__update_offline_repo()
            
            if args.online:
                self.__cleanup()
                self.__build(offline=False)
            
            if args.offline:
                self.__cleanup()
                if not self.__check_offline_repo():
                    print("[WARNING] Офлайн репозиторий будет автоматически создан.")
                    self._execute("/usr/bin/echo \"[WARNING] Офлайн репозиторий будет автоматически создан.\"")
                    self.__update_offline_repo()
                self.__build(offline=True)
            self._execute("__INTERNAL_FINISH")
            self._execute_commands()
            return
        
        try:
            scaling = int(args.scaling)
        except ValueError:
            print("[ERROR] Неверно указано мастабирование. Возврат к значению по умолчанию в 100%")
            scaling = 100
        scaling = round(scaling/100, 2)
        set_widget_scaling(scaling)
        set_window_scaling(scaling)

        if args.dark_theme:
            set_appearance_mode("dark")

        super().__init__()

        self.title("Сборщик Secux Linux")

        self.bin = f"{WORKDIR}/bin"
        self.output = f"{WORKDIR}/builds"


        label = CTkLabel(self, text="Программа для сборки Secux Linux")
        self.work_dir = CTkLabel(self, text=f"Рабочая папка: {self.bin}")
        self.work_dir_btn = CTkButton(self, text="Сменить папку", command=self.__bin_handler)
        self.output_dir = CTkLabel(self, text=f"Папка для ISO образов: {self.output}")
        self.output_dir_btn = CTkButton(self, text="Сменить папку", command=self.__output_handler)

        self.online_checkbox = CTkCheckBox(self, text='Онлайн сборка')
        self.offline_checkbox = CTkCheckBox(self, text='Офлайн сборка')
        online_label = CTkLabel(self, text="Минимальный ISO образ. Для установки\nсистемы потребуется подключение к интернету.")
        offline_label = CTkLabel(self, text="ISO образ с всеми приложениями и \nпакетами, необходимыми для установки.")

        update_offline_apps_label = CTkLabel(self, text="Secux Installer, Secux Manager, KIRTapp")
        self.update_offline_apps = CTkCheckBox(self, text="Скачать/обновить приложения")

        update_offline_repo_label = CTkLabel(self, text="Офлайн репозиторий содержит систему,\nвсе необходимые пакеты и зависимости\nдля установки Secux Linux.")
        self.update_offline_repo = CTkCheckBox(self, text="Скачать/обновить офлайн репозиторий")

        build = CTkButton(self, text="Запустить", command=self._build_ui)

        label.grid(row=0, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.work_dir.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        self.work_dir_btn.grid(row=1, column=1, padx=15, pady=5, sticky="nsew")
        self.output_dir.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        self.output_dir_btn.grid(row=2, column=1, padx=15, pady=5, sticky='nsew')

        self.online_checkbox.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")
        online_label.grid(row=3, column=1, padx=15, pady=5, sticky="nsew")
        self.offline_checkbox.grid(row=4, column=0, padx=15, pady=5, sticky="nsew")
        offline_label.grid(row=4, column=1, padx=15, pady=5, sticky="nsew")
        update_offline_apps_label.grid(row=5, column=1, padx=15, pady=5, sticky="nsew")
        self.update_offline_apps.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        update_offline_repo_label.grid(row=6, column=1, padx=15, pady=5, sticky="nsew")
        self.update_offline_repo.grid(row=6, column=0, padx=15, pady=5, sticky='nsew')
        build.grid(row=7, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")

    def __bin_handler(self):
        dir = filedialog.askdirectory()
        if dir:
            self.bin = dir
            self.work_dir.configure(text=f"Рабочая папка: {self.bin}")        
    
    def __output_handler(self):
        dir = filedialog.askdirectory()
        if dir:
            self.output = dir
            self.output_dir.configure(text=f"Папка для ISO образов: {self.output}")
    
    def _check_dependencies(self) -> bool:
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
        notification_pool = ""
        for requirement in requirements.items():
            if not os.path.isfile(requirement[0]):
                text = f"[ERROR] {requirement[0]} не найден. Для установки пакета используйте: pacman -S {requirement[1]}"
                print(text)
                notification_pool += text + "\n"
                errors = True
        if errors: 
            Notification(notification_pool)
            return False
        return True

    def _check_internet_connection(self) -> bool:
        try:
            answ = get("http://gstatic.com/generate_204", timeout=5)
        except ConnectionError:
            return False
        if answ.status_code != 204:
            return False
        return True

    def __check_offline_repo(self) -> bool:
        db_path = os.path.join(OFFLINE_REPO_PATH, "offline-repo.db")
        if os.path.isfile(db_path):
            return True
        else:
            return False

    def __update_apps(self):
        dir = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer"
        self._execute(f"/usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"")
        self._execute(f"/usr/bin/git clone --depth=1 {self.repos['secux-installer']} \"{dir}\"")

        dir = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-apps"
        self._execute(f"/usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"")
        self._execute(f"/usr/bin/git clone --depth=1 {self.repos['secux-apps']} \"{dir}\"")

        dir = f"{WORKDIR}/releng/airootfs/usr/local/share/KIRTapp"
        self._execute(f"/usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"")
        self._execute(f"/usr/bin/git clone --depth=1 {self.repos['KIRTapp']} \"{WORKDIR}/releng/airootfs/usr/local/share/KIRTapp\"")

    def __update_offline_repo(self) -> bool:
        self._execute(f"/usr/bin/test -e {OFFLINE_REPO_PATH} && /usr/bin/rm -rf {OFFLINE_REPO_PATH}")
        self._execute(f"/usr/bin/mkdir -p {OFFLINE_REPO_PATH}")

        self._execute(f"/usr/bin/grep -q '^\\[kolbanidze\\]' /etc/pacman.conf || /usr/bin/echo \"[kolbanidze]\nServer = https://kolbanidze.github.io/secux-repo/x86_64/\n\" >> /etc/pacman.conf")
        self._execute(f"/usr/bin/pacman-key --populate --populate-from \"{WORKDIR}/releng/airootfs/usr/share/pacman/keyrings/\" kolbanidze")
        
        self._execute(f"/usr/bin/pacman -Sywu --noconfirm --cachedir {OFFLINE_REPO_PATH} {PACKAGES}")
        self._execute(f"/usr/bin/repo-add {OFFLINE_REPO_PATH}/offline-repo.db.tar.zst {OFFLINE_REPO_PATH}/*[^sig]")

    def __is_kolbanidze_trusted(self) -> bool:
        try:
            result = subprocess.run("/usr/bin/pacman-key --list-keys CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE",
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            return "CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE" in result.stdout
        except Exception as e:
            print(f"[WARNING] Произошла ошибка в время проверки доверия к ключам kolbanidze: {e}")
            return False

    def __cleanup(self) -> None:
        # Bin/
        self._execute(f"/usr/bin/test -e \"{self.bin}\" && /usr/bin/rm -rf \"{self.bin}\" || /usr/bin/mkdir -p \"{self.bin}\"")
        
        # Builds/
        self._execute(f"/usr/bin/test -e \"{self.output}\" || /usr/bin/mkdir -p \"{self.output}\"")
            
    def _execute(self, command: str):
        self.commands.append(command)


    def _execute_commands(self):
        def run_commands():
            try:
                for command_ in self.commands:
                    if command_ == "__INTERNAL_FINISH":
                        print("Программа успешно завершила свою работу.")
                        Notification(message="Программа успешно завершила свою работу.", icon="greencheck.png", title="Успех")
                        break
                    command = "/usr/bin/stdbuf -oL " + command_

                    print(f"Выполнение: {command}")
                    process = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True,
                        text=True,
                        executable="/bin/bash",
                        bufsize=1
                    )

                    def update_console(text):
                        self.console.configure(state="normal")
                        self.console.insert(END, text)
                        self.console.see(END)
                        self.console.configure(state="disabled")

                    for line in process.stdout:
                        print(line, end="")
                        if not args.cli: self.console.after(0, update_console, line)

                    for line in process.stderr:
                        print(line, end="")
                        if not args.cli: self.console.after(0, update_console, line)

                    process.wait()
                    if process.returncode != 0 and command_[:13] != "/usr/bin/test":
                        print(f"Произошла ошибка в время выполнения команды: {command}.")
                        Notification(f"Произошла ошибка в время выполнения команды: {command}.")
                        break
                    print("\n")

            except Exception as e:
                print(f"Error: {str(e)}\n")
                if not args.cli: self.console.after(0, update_console, f"Error: {str(e)}\n")
        
        if not args.cli:
            threading.Thread(target=run_commands, daemon=True).start()
        else:
            run_commands()

    def _build_ui(self):
        self.commands = []

        if not os.path.isdir(f"{WORKDIR}/releng"):
            Notification(f"[ERROR] Директория releng не найдена. Создание образа Secux Linux невозможно.")
            print(f"[ERROR] Директория releng не найдена. Создание образа Secux Linux невозможно.")
            return
        
        if not self._check_internet_connection():
            Notification("[ERROR] Для сборки Secux Linux необходимо стабильное подключеие к интернету.")
            print("[ERROR] Для сборки Secux Linux необходимо стабильное подключеие к интернету.")
            return
        
        if not self._check_dependencies():
            print("[ERROR] Не установлены необходимые зависимости.")
            return

        online = self.online_checkbox.get()
        offline = self.offline_checkbox.get()
        update_apps = self.update_offline_apps.get()
        update_repo = self.update_offline_repo.get()

        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x400")
        calm_emoji = CTkImage(light_image=Image.open(f"{WORKDIR}/images/calm.png"), dark_image=Image.open(f"{WORKDIR}/images/calm.png"), size=(80, 80))
        calm_emoji_label = CTkLabel(self, text="", image=calm_emoji)
        calm_emoji_label.pack(padx=10, pady=10)
        label = CTkLabel(self, text="Пока можете откинуться на спинку стула.\nТехническая информация о процессе сборки:")
        label.pack(padx=10, pady=10)
        self.console = CTkTextbox(self)
        self.console.pack(padx=10, pady=10, expand=True, fill="both")

        if update_apps:
            self.__update_apps()

        if update_repo:
            self.__update_offline_repo()

        if online:
            self.__cleanup()
            self.__build(offline=False)
        
        if offline:
            self.__cleanup()
            if not self.__check_offline_repo():
                print("[WARNING] Офлайн репозиторий будет автоматически создан.")
                self._execute("/usr/bin/echo \"[WARNING] Офлайн репозиторий будет автоматически создан.\"")
                self.__update_offline_repo()
            self.__build(offline=True)
        self._execute("__INTERNAL_FINISH")
        self._execute_commands()
    
    def __build(self, offline: bool) -> None:
        self._execute(f"/usr/bin/mkdir -p \"{WORKDIR}/releng/airootfs/var/cache/pacman\"")
        
        dir = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer"
        self._execute(f"/usr/bin/test -e \"{dir}/main.py\" || {{ /usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"; /usr/bin/git clone --depth=1 {self.repos['secux-installer']} \"{dir}\"; }}")
        
        if offline:            
            dir = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-apps"
            self._execute(f"/usr/bin/test -e \"{dir}/manager.py\" || {{ /usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"; /usr/bin/git clone --depth=1 {self.repos['secux-apps']} \"{dir}\"; }}")

            dir = f"{WORKDIR}/releng/airootfs/usr/local/share/KIRTapp"
            self._execute(f"/usr/bin/test -e \"{dir}/app_script/app.py\" || {{ /usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"; /usr/bin/git clone --depth=1 {self.repos['KIRTapp']} \"{dir}\"; }}")
        else:
            dir = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-apps"
            self._execute(f'/usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"')
            dir = f"{WORKDIR}/releng/airootfs/usr/local/share/KIRTapp"
            self._execute(f'/usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"')
        
        self._execute(f"/usr/bin/touch \"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/production.conf\"")

        file = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/offline_installation.conf"
        if offline:
            self._execute(f"/usr/bin/test -e \"{file}\" || /usr/bin/touch \"{file}\"")
        else:
            self._execute(f"/usr/bin/test -e \"{file}\" && /usr/bin/rm \"{file}\"")
        
        if offline:
            dir = f"{WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo"
            self._execute(f"/usr/bin/test -e \"{dir}\" && /usr/bin/rm -rf \"{dir}\"")
            self._execute("echo [INFO] Сборка офлайн образа. Копирую офлайн репозиторий.")
            self._execute(f"/usr/bin/rsync -aAXHv --info=progress2 {OFFLINE_REPO_PATH}/* \"{dir}\"")
        else:
            dir = f"{WORKDIR}/releng/airootfs/var/cache/pacman/offline-repo"
            self._execute(f"/usr/bin/test -e \"{dir}\" && {{ /usr/bin/test -z \"$(ls -A \"{dir}\")\"; /usr/bin/rm -rf \"{dir}/*\"; }} ")
            dir = f"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages"
            self._execute(f"/usr/bin/test -e \"{dir}\" && {{ /usr/bin/test -z \"$(ls -A \"{dir}\")\"; /usr/bin/rm -rf \"{dir}/*\"; }} ")
        
        if offline:
            self._execute(f"/usr/bin/cp \"{WORKDIR}/releng/airootfs/etc/pacman_offline.conf\" \"{WORKDIR}/releng/airootfs/etc/pacman.conf\"")
        else:
            self._execute(f"/usr/bin/cp \"{WORKDIR}/releng/airootfs/etc/pacman_online.conf\" \"{WORKDIR}/releng/airootfs/etc/pacman.conf\"")
        
        if offline:
            self._execute(f"/usr/bin/chmod +x \"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/collect_python_packages.sh\"")
            self._execute(f"/usr/bin/bash \"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/collect_python_packages.sh\" \"{WORKDIR}/releng/airootfs/usr/local/share/secux-installer/python_packages\"")

        if not self.__is_kolbanidze_trusted():
            self._execute("/usr/bin/echo [WARNING] Добавление ключа kolbanidze в список доверенных.")
            self._execute(f"/usr/bin/pacman-key --populate --populate-from \"{WORKDIR}/releng/airootfs/usr/share/pacman/keyrings/\" kolbanidze")

        self._execute(f"/usr/bin/mkarchiso -v -w \"{self.bin}\" -o \"{self.bin}\" \"{WORKDIR}/releng\"")
        buildtype = "offline" if offline else "online"
        build = f"SecuxLinux-{buildtype}-{datetime.today().strftime('%Y-%m-%d_%H-%M')}.iso"
        self._execute(f"/usr/bin/mv \"{os.path.join(self.bin, 'Secux-Linux-x86_64.iso')}\" \"{os.path.join(self.output, build)}\"")
        self._execute(f"/usr/bin/echo \"ISO образ {build} успешно сохранён в {self.output}.\"")
        

if __name__ == "__main__":
    if args.cli:
        App()
    else:
        App().mainloop()
